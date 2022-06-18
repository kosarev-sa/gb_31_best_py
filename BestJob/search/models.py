from django.db import models

# Create your models here.

class EducationLevel(models.IntegerChoices):
    """Уровень образования (выбор одного значения)"""
    SECONDARY = 1, "Среднее"
    SPEC_SEC = 2, "Среднее специальное"
    INC_HIGHER = 3, "Неоконченное высшее"
    HIGHER = 4, "Высшее"
    BACHELOR = 5, "Бакалавр"
    MASTER = 6, "Магистр"
    CANDIDATE = 7, "Кандидат наук"
    DOCTOR = 8, "Доктор наук"


class Moving(models.IntegerChoices):
    """Переезд (выбор одного значения)"""
    UNREAL = 1, "Невозможен"
    REAL = 2, "Возможен"
    DESIRE = 3, "Желателен"


class MainSkills(models.Model):
    """Ключевые навыки. code: DJANGO, skill: Django Framework"""
    code = models.CharField(max_length=10, unique=True)
    skill = models.CharField(max_length=100, unique=True)


class Languages(models.Model):
    """Языки. code: ENG, language: английский"""
    code = models.CharField(max_length=3, unique=True)
    language = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.language

class LanguageLevels(models.Model):
    """Уровень владения языком. code: A1, level: Начальный"""
    code = models.CharField(max_length=3, unique=True)
    level = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.level


class Employments(models.Model):
    """Занятость. code: FULL, employment: Полная занятость"""
    code = models.CharField(max_length=10, unique=True)
    employment = models.CharField(max_length=100, unique=True)


class WorkSchedules(models.Model):
    """График работы. code: FULL, schedule: Полный день"""
    code = models.CharField(max_length=10, unique=True)
    schedule = models.CharField(max_length=100, unique=True)


class Category(models.Model):
    """Специализации. code: PROG, name: Программист"""
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Currency(models.IntegerChoices):
    """Валюта (выбор одного значения)"""
    RUB = 1, 'Рубли'
    USD = 2, 'Доллары, США'
    EUR = 3, 'Евро'
    KZT = 4, 'Тенге, Казахстан'
