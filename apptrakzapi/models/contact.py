from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=25)
    email = models.CharField(max_length=75)
