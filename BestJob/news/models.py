from django.db import models


# Create your models here.
from users.models import ModeratorProfile


class News(models.Model):
    """model for news on main page"""
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, db_index=True)
    updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    author = models.ForeignKey(ModeratorProfile, verbose_name='Создал', null=False, db_index=True, on_delete=models.PROTECT)
    title = models.CharField(verbose_name='Заголовок', blank=False, null=False, max_length = 500)
    body = models.TextField(verbose_name='Содержание', blank=False)
    is_active = models.BooleanField(verbose_name='Aктивена', default=True)
    image = models.ImageField(upload_to='news_images', blank=False)
