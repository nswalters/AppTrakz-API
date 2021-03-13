from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from apptrakzapi.models import Contact, Job


class JobContact(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE_CASCADE

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
