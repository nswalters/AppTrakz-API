from django.db import models
from django.contrib.auth.models import User

from apptrakzapi.models import Job


class Application(models.Model):

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField()
