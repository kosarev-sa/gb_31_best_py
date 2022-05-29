from django.db import models


# Create your models here.

class ApprovalStatus(models.Model):
    """model of status approval"""
    status = models.CharField(max_length=100, unique=True)
