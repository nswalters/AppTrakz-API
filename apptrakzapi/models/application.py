from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User


class Application(models.Model):

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    job = models.ForeignKey("Job", on_delete=models.DO_NOTHING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField()

    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'job'],
                                        name="unique_job_application_user")]
