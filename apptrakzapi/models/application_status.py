from django.db import models

from apptrakzapi.models import Application


class ApplicationStatus(models.Model):

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    status = models.ForeignKey("Status", on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=500, null=True, blank=True)
    is_current = models.BooleanField()
