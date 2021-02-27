from django.db import models
from django.contrib.auth.models import User
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from apptrakzapi.models import Company


class CompanyNote(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
