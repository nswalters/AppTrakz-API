from django.db import models


class SocialMediaType(models.Model):

    name = models.CharField(max_length=50)
