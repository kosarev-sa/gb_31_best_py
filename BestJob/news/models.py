from django.db import models


# Create your models here.
from users.models import User


class News(models.Model):
    """model for news on main page"""
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, db_index=True)
    updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    author = models.ForeignKey(User, verbose_name='Создал', null=False, db_index=True, on_delete=models.PROTECT)
    title = models.TextField(verbose_name='Заголовок', blank=True, null=False)
    body = models.TextField(verbose_name='Содержание', blank=True)
    is_active = models.BooleanField(verbose_name='Aктивена', default=True)


