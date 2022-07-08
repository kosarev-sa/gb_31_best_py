from django.db import models

# Create your models here.
from approvals.models import ApprovalStatus
from users.models import EmployerProfile, WorkerProfile
from search.models import Employments, WorkSchedules, MainSkills, Category, Currency

EXPERIENCE = (
        ('NO', 'От 1 года до 3 лет'),
        ('EXP', 'От 3 до 6 лет'),
        ('BIG', 'Более 6 лет')
    )


class Vacancy(models.Model):
    """Вакансии"""
    employer_profile = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, verbose_name='Компания | ИП')
    status = models.ForeignKey(ApprovalStatus, default=1, on_delete=models.CASCADE, verbose_name='Статус модерации')
    specialization = models.ForeignKey(Category, default=1, on_delete=models.CASCADE, verbose_name='Специализация')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Вакансия активна')
    name = models.CharField(max_length=256, blank=True, verbose_name='Название вакансии')
    experience = models.CharField(max_length=3, choices=EXPERIENCE, blank=True, verbose_name='Опыт')
    city = models.CharField(max_length=20, blank=True, verbose_name='Вакансия в городе')
    description = models.TextField(blank=True, null=True, verbose_name='Описание вакансии')
    salary_from = models.DecimalField(max_digits=8, decimal_places=1, blank=True, null=True, verbose_name='доход от')
    salary_to = models.DecimalField(max_digits=8, decimal_places=1, blank=True, null=True, verbose_name='доход до')
    currency = models.PositiveSmallIntegerField(choices=Currency.choices, default=Currency.RUB, verbose_name='валюта')
    salary_on_hand = models.BooleanField(default=True, blank=True, verbose_name='Зарплата на руки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    moderators_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    #
    # def is_favorite(self, worker_id):
    #     worker = WorkerProfile.objects.get(id=worker_id)
    #     wf = WorkerFavorites.objects.filter(worker_profile=worker, vacancy=self)
    #     if wf:
    #         return True
    #     else:
    #         return False