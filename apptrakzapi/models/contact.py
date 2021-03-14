from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE


class Contact(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE_CASCADE

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=25)
    email = models.CharField(max_length=75)
