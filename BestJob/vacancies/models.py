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
    employer_profile = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    status = models.ForeignKey(ApprovalStatus, default=1, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, db_index=True)
    name = models.CharField(max_length=256, blank=True, verbose_name='Название вакансии')
    experience = models.CharField(max_length=3, choices=EXPERIENCE, blank=True, verbose_name='Опыт')
    city = models.CharField(max_length=20, blank=True, verbose_name='Вакансия в городе')
    description = models.CharField(max_length=256, blank=True, verbose_name='Описание вакансии')
    salary_from = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='доход от')
    salary_to = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='доход до')
    currency = models.PositiveSmallIntegerField(choices=Currency.choices, default=Currency.RUB)
    salary_on_hand = models.BooleanField(default=True, blank=True, verbose_name='Зарплата на руки')

    def __unicode__(self):
        return self.name


class Skills(models.Model):
    """Ключевые навыки"""
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    skill = models.ForeignKey(MainSkills, on_delete=models.CASCADE)


class EmploymentType(models.Model):
    """Тип занятости"""
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    employment = models.ForeignKey(Employments, on_delete=models.CASCADE)


class WorkingHours(models.Model):
    """Режим работы"""
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    schedule = models.ForeignKey(WorkSchedules, on_delete=models.CASCADE)


class SelectedVacancies(models.Model):
    """Избранные вакансии"""
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    worker_profile = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE)

