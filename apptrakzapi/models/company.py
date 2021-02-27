from django.db import models
from django.contrib.auth.models import User
from safedelete.models import SafeDeleteModel, SOFT_DELETE


class Company(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zipcode = models.IntgerField()
    website = models.CharField(max_length=100)
