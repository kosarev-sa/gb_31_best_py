from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """группы пользователей: Модератор, соискатель, работодатель"""
    role_name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    """модель пользователя. одна на всех. отличается только группой"""
    role = models.ForeignKey(Role, null=True, db_constraint=False, on_delete=models.CASCADE)


class EmployeeProfile(models.Model):
    """профиль для соискателя"""
    user = models.ForeignKey(User, null=False, db_index=True, on_delete=models.CASCADE)
    data = models.TextField()


class EmployerProfile(models.Model):
    """профиль для работодателя"""
    user = models.ForeignKey(User, null=False, db_index=True, on_delete=models.CASCADE)
    data = models.TextField()


class ModeratorProfile(models.Model):
    """профиль для модератора"""
    user = models.ForeignKey(User, null=False, db_index=True, on_delete=models.CASCADE)
    data = models.TextField()
