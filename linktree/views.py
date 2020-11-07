from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, DeletionMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from linktree.models import URL, SocialMedia
from linktree.forms import AddURL, AddSocial
from user_registration.views import profile_view

@login_required
def add_url(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('view_profile', username= username)    

    form = AddURL()
    if request.method == 'POST':
        form = AddURL(request.POST)
        if form.is_valid():
            if user:
                url = form.save(commit=False)
                url.user = user
                url.save()
                return profile_view(request, username)
    else:
        print(form.errors)
    context_dict = {'form':form, 'current_user': user}
    return render(request, 'linktree/add-url.html', context_dict)

@login_required
def add_social(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('view_profile', username=username)    

    form = AddSocial()
    if request.method == 'POST':
        form = AddSocial(request.POST)
        if form.is_valid():
            if user:
                social = form.save(commit=False)
                social.user = user
                social.save()
                return profile_view(request, username)
    else:
        print(form.errors)
    context_dict = {'form':form, 'current_user': user}
    return render(request, 'linktree/add-social.html', context_dict)

class DeleteSocial(DeleteView):
    model = SocialMedia

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.
        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
            if obj.user == self.request.user:
                return obj
            else:
                return HttpResponse("<a>not your url </a>")
        except queryset.model.DoesNotExist:
            raise Http404(("No %(verbose_name)s found matching the query") %
                        {'verbose_name': queryset.model._meta.verbose_name})


    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.model = self.get_object()
        if self.model.user == request.user:
            self.model.delete()
            success_url = self.get_success_url()
            return HttpResponseRedirect(success_url)
        else:
            return HttpResponse('<h1>Not your link!</h1>')
    
    def get_success_url(self):
        username = self.kwargs['username']
        return reverse_lazy('url_list', kwargs={'username': username})

class DeleteURL(DeleteView):
    model = URL

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.
        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
            if obj.user == self.request.user:
                return obj
            else:
                return HttpResponse("<a>Not Your Social! </a>")
        except queryset.model.DoesNotExist:
            raise Http404(("No %(verbose_name)s found matching the query") %
                        {'verbose_name': queryset.model._meta.verbose_name})


    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.model = self.get_object()
        if self.model.user == request.user:
            self.model.delete()
            success_url = self.get_success_url()
            return HttpResponseRedirect(success_url)
        else:
            return HttpResponse('<h1>Not Your Social!</h1>')
    
    def get_success_url(self):
        username = self.kwargs['username']
        return reverse_lazy('url_list', kwargs={'username': username})

def social_and_url_list(request, username):
    """ 
    Listing current user's links and socials for editing purposes
    """
    try:
        current_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse('<h1>User DNE!</h1>') 

    socials = SocialMedia.objects.filter(user=current_user)
    urls = URL.objects.filter(user=current_user)

    context_dict = {'socials': socials, 'urls': urls, 'current_user' : current_user}
    return render(request, 'linktree/list.html', context_dict)

