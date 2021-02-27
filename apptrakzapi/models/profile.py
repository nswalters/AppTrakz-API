from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    bio = models.TextField()
    profile_image = models.ImageField(
        upload_to='profile_images', height_field=None, width_field=None, max_length=None, null=True)
