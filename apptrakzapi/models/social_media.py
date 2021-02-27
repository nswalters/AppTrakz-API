from django.db import models
from apptrakzapi.models import Profile, SocialMediaType


class SocialMedia(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    profile_id = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    type_id = models.ForeignKey(SocialMediaType, on_delete=models.DO_NOTHING)
