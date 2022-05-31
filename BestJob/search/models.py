from django.db import models

# Create your models here.


class MainSkills(models.Model):
    """Ключевые навыки. code: DJANGO, skill: Django Framework"""
    code = models.CharField(max_length=10, unique=True)
    skill = models.CharField(max_length=100, unique=True)


class Languages(models.Model):
    """Языки. code: ENG, language: английский"""
    code = models.CharField(max_length=3, unique=True)
    language = models.CharField(max_length=100, unique=True)


class LanguageLevels(models.Model):
    """Уровень владения языком. code: A1, level: Начальный"""
    code = models.CharField(max_length=3, unique=True)
    level = models.CharField(max_length=100, unique=True)


class Employments(models.Model):
    """Занятость. code: FULL, employment: Полная занятость"""
    code = models.CharField(max_length=10, unique=True)
    employment = models.CharField(max_length=100, unique=True)


class WorkSchedules(models.Model):
    """График работы. code: FULL, schedule: Полный день"""
    code = models.CharField(max_length=10, unique=True)
    schedule = models.CharField(max_length=100, unique=True)

