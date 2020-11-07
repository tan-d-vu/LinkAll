from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from user_registration.models import Profile
from user_registration.forms import ProfileForm
from linktree.models import URL, SocialMedia
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.conf import settings 
from django.core.mail import send_mail 
def index(request):
    return render(request, 'user-reg/index.html', {})

@login_required()
def profile_update(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    
    profile = Profile.objects.get_or_create(user=user)[0]

    profile_form = ProfileForm({'logo': profile.logo, 'background': profile.background,
                                'bio' : profile.bio, 'display_name' : profile.display_name})

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save(commit=True)
            return redirect('view_profile', user.username)
        else:
            print(profile_form.errors)
    
    return render(request, 'user-reg/profile-update.html', {'profile_form' : profile_form, 'current_user' : user,})

def profile_view(request, username):
    context_dict = {}
    try:
        user = User.objects.get(username=username)
        urls = URL.objects.filter(user=user)
        socials = SocialMedia.objects.filter(user=user)
        context_dict['current_profile'] = user
        context_dict['urls'] = urls
        context_dict['socials'] = socials
    except User.DoesNotExist:
        context_dict['current_profile'] = None
        context_dict['urls'] = None
        context_dict['socials'] = None
    return render(request, 'user-reg/profile-view.html', context_dict)


