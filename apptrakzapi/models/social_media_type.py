from django.db import models


class SocialMediaType(models.Model):

    type = models.CharField(max_length=50)
