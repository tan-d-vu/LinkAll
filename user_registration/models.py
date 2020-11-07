from django.db import models
from django.contrib.auth.models import User

# User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    display_name = models.CharField(max_length = 200, blank = True)
    bio = models.TextField()
    logo = models.ImageField(blank = True, upload_to = "logo")
    background = models.ImageField(blank = True, upload_to = "background")

    def __str__(self):
        return self.user.username