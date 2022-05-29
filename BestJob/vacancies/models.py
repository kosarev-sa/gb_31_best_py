from django.db import models

# Create your models here.
from approvals.models import ApprovalStatus
from users.models import EmployerProfile


class Vacancy(models.Model):
    """резюме"""
    employee_profile_id = models.ForeignKey(EmployerProfile, db_constraint=False, on_delete=models.CASCADE)
    status = models.ForeignKey(ApprovalStatus, db_constraint=False, on_delete=models.CASCADE)
    data = models.TextField()