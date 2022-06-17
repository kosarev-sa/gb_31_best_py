from django.db import models

# Create your models here.
from approvals.models import ApprovalStatus
from search.models import Languages, LanguageLevels, Employments, WorkSchedules, MainSkills, Moving, EducationLevel, Category, Currency
from users.models import WorkerProfile, EmployerProfile
from vacancies.models import Vacancy


class CV(models.Model):
    """Резюме"""
    worker_profile = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE)
    status = models.ForeignKey(ApprovalStatus, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, db_index=True)
    speciality = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    post = models.CharField(max_length=256, blank=True, null=True)
    skills = models.CharField(max_length=256, blank=True, null=True)
    education_level = models.PositiveSmallIntegerField(choices=EducationLevel.choices, default=EducationLevel.HIGHER)
    moving = models.PositiveSmallIntegerField(choices=Moving.choices, default=Moving.UNREAL, null=True)
    salary = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Зарплата')
    currency = models.PositiveSmallIntegerField(choices=Currency.choices, default=Currency.RUB, null=True)


class CVSkills(models.Model):
    """Ключевые навыки"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    skill = models.ForeignKey(MainSkills, on_delete=models.CASCADE)


class Education(models.Model):
    """Образование"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    date_end = models.IntegerField(null=True)
    name = models.CharField(max_length=256)
    department = models.CharField(max_length=256)
    specialty = models.CharField(max_length=256)


class CVMonths(models.IntegerChoices):
    JAN = 1, "Январь"
    FEB = 2, "Февраль"
    MAR = 3, "Март"
    APR = 4, "Апрель"
    MAY = 5, "Май"
    JUN = 6, "Июнь"
    JUL = 7, "Июль"
    AUG = 8, "Август"
    SEP = 9, "Сентябрь"
    OCT = 10, "Октябрь"
    NOV = 11, "Ноябрь"
    DEC = 12, "Декабрь"

class Experience(models.Model):

    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    month_begin = models.PositiveSmallIntegerField(choices=CVMonths.choices, default=CVMonths.JAN)
    year_begin = models.IntegerField(null=True)
    month_end = models.PositiveSmallIntegerField(choices=CVMonths.choices, default=CVMonths.JAN)
    year_end = models.IntegerField(null=True)
    name = models.CharField(max_length=256)
    post = models.CharField(max_length=128)
    stack = models.CharField(max_length=256, null=True)
    responsibilities = models.TextField(max_length=2000, null=True)


class LanguagesSpoken(models.Model):
    """Владение языками в резюме (возможно несколько значений)"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE)
    level = models.ForeignKey(LanguageLevels, on_delete=models.CASCADE)


class CVEmployment(models.Model):
    """Занятость в резюме (возможно несколько значений)"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    employment = models.ForeignKey(Employments, on_delete=models.CASCADE)


class CVWorkSchedule(models.Model):
    """График работы в резюме (возможно несколько значений)"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    schedule = models.ForeignKey(WorkSchedules, on_delete=models.CASCADE)


class SelectedCV(models.Model):
    """Избранные резюме"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    employer_profile = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)


class ConnectVacancyCv(models.Model):
    """Связь отклика, вакансии и резюме"""
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    status_worker = models.BooleanField(default=None)
    status_employer = models.BooleanField(default=None)