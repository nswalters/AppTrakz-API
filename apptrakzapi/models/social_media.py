from django.db import models
from apptrakzapi.models import Profile


class SocialMedia(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.ForeignKey("SocialMediaType", on_delete=models.DO_NOTHING)
