from django.db import models
from django.contrib.auth.models import User
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from apptrakzapi.models import Company


class Job(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE_CASCADE

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role_title = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    qualifications = models.CharField(max_length=500)
    post_link = models.URLField()
    salary = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField()
