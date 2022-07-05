import datetime
from datetime import timedelta


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

from BestJob import settings

from approvals.models import ApprovalStatus


class Role(models.Model):
    """группы пользователей: Модератор, соискатель, работодатель"""
    role_name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    """модель пользователя. одна на всех. отличается только группой"""
    role = models.ForeignKey(Role, null=True, db_constraint=False, on_delete=models.CASCADE)
    # ключ используемый для подтверждения email
    activation_key = models.CharField(max_length=128, null=True, blank=True)
    # дата создания ключа для проверки работоспособности ключа (действует 48 часов)
    activation_key_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def is_activation_key_expired(self):
        """метод для проверки, что ключ проверки email не просрочен"""
        if now() <= self.activation_key_created + timedelta(hours=settings.USER_EMAIL_KEY_LIFETIME):
            return False
        return True


class WorkerProfile(models.Model):
    """профиль для соискателя"""
    user = models.ForeignKey(User, null=False, db_index=True, on_delete=models.CASCADE)
    name = models.CharField('ФИО', max_length=80, blank=True)
    image = models.ImageField(upload_to='worker_photo', blank=True)
    city = models.CharField('Город проживания', max_length=80, blank=True)
    phone_number = models.CharField('Телефон для связи', max_length=12, blank=True)
    gender = models.CharField('Пол', max_length=1, blank=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    data = models.TextField('О себе', blank=True)


class EmployerProfile(models.Model):
    """профиль для работодателя"""
    user = models.ForeignKey(User, null=False, db_index=True, on_delete=models.CASCADE)
    name = models.CharField('Название компании', max_length=80, blank=True)
    image = models.ImageField(upload_to='company_images', blank=True)
    status = models.ForeignKey(ApprovalStatus, default=1, verbose_name='Статус', on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, db_index=True)
    city = models.CharField('Город местонахождения', max_length=80, blank=True)
    data = models.TextField('Описание компании', blank=True)
    moderators_comment = models.TextField(max_length=5000, blank=True, null=True)

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
    name = models.CharField('ФИО', max_length=80, blank=True)
    image = models.ImageField(upload_to='moderator_photo', blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
