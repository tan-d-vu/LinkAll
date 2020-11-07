from django import forms
from django.contrib.auth.models import User
from user_registration.models import  Profile
from linktree.models import URL, SocialMedia

class AddURL(forms.ModelForm):
    title = forms.CharField(max_length=300, required=True)
    url = forms.URLField(required=True)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)  

    class Meta:
        model = URL
        exclude = ('user',)

class AddSocial(forms.ModelForm):
    SOCIAL_MEDIA_CHOICES = (
        ("fa-facebook", "Facebook"),
        ("fa-instagram", "Instagram"),
        ("fa-youtube", "YouTube"),
        ("fa-twitter", "Twitter"),
        ("fa-spotify", "Spotify"),
        ("fa-reddit", "Reddit")
    )
    url = forms.URLField(required=True)
    name = forms.ChoiceField(choices=SOCIAL_MEDIA_CHOICES, required=True)

    class Meta:
        model = SocialMedia
        exclude = ('user',)