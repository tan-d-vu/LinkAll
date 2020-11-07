from django import forms
from django.contrib.auth.models import User
from user_registration.models import  Profile
from registration.forms import RegistrationFormUniqueEmail, RegistrationForm

class ProfileForm(forms.ModelForm):
    logo = forms.ImageField(required = False)
    background = forms.ImageField(required = False)
    display_name = forms.CharField(required = False, max_length = 200)
    bio =  forms.CharField(widget=forms.Textarea, required = False)

    class Meta:
        model = Profile
        exclude = ('user' ,)