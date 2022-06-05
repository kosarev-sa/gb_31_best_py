from django.db import models

# Create your models here.
from approvals.models import ApprovalStatus
from users.models import EmployerProfile
from search.models import Employments, WorkSchedules, MainSkills, Category

EXPERIENCE = (
        ('NO', 'От 1 года до 3 лет'),
        ('EXP', 'От 3 до 6 лет'),
        ('BIG', 'Более 6 лет')
    )


class Vacancy(models.Model):
    """Вакансии"""
    employer_profile = models.ForeignKey(EmployerProfile, db_constraint=False, on_delete=models.CASCADE)
    status = models.ForeignKey(ApprovalStatus, db_constraint=False, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, db_index=True)
    name = models.CharField(max_length=256, blank=True, verbose_name='Название вакансии')
    experience = models.CharField(max_length=3, choices=EXPERIENCE, blank=True, verbose_name='Опыт')
    city = models.CharField(max_length=20, blank=True, verbose_name='Вакансия в городе')
    description = models.CharField(max_length=256, blank=True, verbose_name='Описание вакансии')


class Salary(models.Model):
    """Предполагаемый уровень дохода в месяц или за объем работ"""

    class Currency(models.IntegerChoices):
        RUB = 1, 'Рубли'
        USD = 2, 'Доллары, США'
        EUR = 3, 'Евро'
        KZT = 4, 'Тенге, Казахстан'

    vacancy = models.ForeignKey(Vacancy, db_constraint=False, on_delete=models.CASCADE)
    salary_from = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='доход от')
    salary_to = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='доход до')
    currency = models.PositiveSmallIntegerField(choices=Currency.choices, default=Currency.RUB)
    is_on_hand = models.BooleanField(default=True, blank=True, verbose_name='Зарплата на руки')


class Skills(models.Model):
    """Ключевые навыки"""
    vacancy = models.ForeignKey(Vacancy, db_constraint=False, on_delete=models.CASCADE)
    skill = models.ForeignKey(MainSkills, db_constraint=False, on_delete=models.CASCADE)


class EmploymentType(models.Model):
    """Тип занятости"""
    vacancy = models.ForeignKey(Vacancy, db_constraint=False, on_delete=models.CASCADE)
    employment = models.ForeignKey(Employments, db_constraint=False, on_delete=models.CASCADE)


class WorkingHours(models.Model):
    """Режим работы"""
    vacancy = models.ForeignKey(Vacancy, db_constraint=False, on_delete=models.CASCADE)
    schedule = models.ForeignKey(WorkSchedules, db_constraint=False, on_delete=models.CASCADE)


class Specialisation(models.Model):
    """Специализация"""
    vacancy = models.ForeignKey(Vacancy, db_constraint=False, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Category, db_constraint=False, on_delete=models.CASCADE)
