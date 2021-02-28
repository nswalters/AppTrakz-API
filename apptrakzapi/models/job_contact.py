from django.db import models

from apptrakzapi.models import Contact, Job


class JobContact(models.Model):

    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
    contact = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)
