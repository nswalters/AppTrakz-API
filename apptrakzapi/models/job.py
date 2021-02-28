from django.db import models
from django.contrib.auth.models import User
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from apptrakzapi.models import Company


class Job(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    role_title = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    qualifications = models.CharField(max_length=500)
    post_link = models.CharField(max_length=200)
    salary = models.CharField(max_length=20, null=True)
    description = models.TextField()
