from django.db import models

# Create your models here.
from approvals.models import ApprovalStatus
from users.models import WorkerProfile


class CV(models.Model):
    """резюме"""
    worker_profile = models.ForeignKey(WorkerProfile, db_constraint=False, on_delete=models.CASCADE)
    status = models.ForeignKey(ApprovalStatus, db_constraint=False, on_delete=models.CASCADE)
    data = models.TextField()
