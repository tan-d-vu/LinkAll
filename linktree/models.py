from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# URLs
class URL(models.Model):
    url = models.URLField(blank = False)
    title = models.CharField(blank = False, max_length = 300)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(URL, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

# Social Media Buttons
class SocialMedia(models.Model):
    url = models.URLField(blank=False)
    # Doesn't need title
    name = models.CharField(blank=False, max_length = 300)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.name
