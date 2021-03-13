from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE


class Application(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE_CASCADE

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey("Job", on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField()

    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'job'],
                                        name="unique_job_application_user")]
