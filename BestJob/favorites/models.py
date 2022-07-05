from django.db import models

# Create your models here.
from cvs.models import CV
from users.models import EmployerProfile, WorkerProfile
from vacancies.models import Vacancy


class EmployerFavorites(models.Model):
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, db_index=True)

    # профиль для работодателя.
    employer_profile = models.ForeignKey(EmployerProfile, verbose_name='Профиль работодателя', on_delete=models.CASCADE)

    cv = models.ForeignKey(CV, verbose_name='Резюме', on_delete=models.CASCADE)

    # Уникальный ключ на 2-е колонки.
    class Meta:
        unique_together = ('employer_profile', 'cv',)


class WorkerFavorites(models.Model):
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, db_index=True)

    # профиль для соискателя.
    worker_profile = models.ForeignKey(WorkerProfile, verbose_name='Профиль соискателя', on_delete=models.CASCADE)

    vacancy = models.ForeignKey(Vacancy, verbose_name='Вакансия', on_delete=models.CASCADE)

    # Уникальный ключ на 2-е колонки.
    class Meta:
        unique_together = ('worker_profile', 'vacancy',)

