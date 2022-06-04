import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from approvals.models import ApprovalStatus


class Role(models.Model):
    """группы пользователей: Модератор, соискатель, работодатель"""
    role_name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    """модель пользователя. одна на всех. отличается только группой"""
    role = models.ForeignKey(Role, null=True, db_constraint=False, on_delete=models.CASCADE)


class WorkerProfile(models.Model):
    """профиль для соискателя"""
    user = models.ForeignKey(User, null=False, db_index=True, on_delete=models.CASCADE)
    data = models.TextField()


class EmployerProfile(models.Model):
    """профиль для работодателя"""
    user = models.ForeignKey(User, null=False, unique=True, db_index=True, \
                                                                       on_delete=models.CASCADE)
    name = models.CharField('Название компании', max_length=80)
    image = models.ImageField(upload_to='company_images', blank=True)
    status = models.ForeignKey(ApprovalStatus, verbose_name='Статус', on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, db_index=True)
    city = models.CharField('Город местонахождения', max_length=80, blank=True)
    data = models.TextField('Описание компании', blank=True)

    #  формат вывода
    def __str__(self):
        return f'{self.name} | {self.city}'

    class Meta:
        """Переопределение названия модели в ед. и мн. числе для админки"""
        verbose_name = "Профиль работодателя"
        verbose_name_plural = "Профили работодателей"


class ModeratorProfile(models.Model):
    """профиль для модератора"""
    user = models.ForeignKey(User, null=False, db_index=True, on_delete=models.CASCADE)
    data = models.TextField()