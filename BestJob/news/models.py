from django.db import models


# Create your models here.

class News(models.Model):
    """model for news on main page"""
    data = models.TextField(blank=True)
