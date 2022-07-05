from django.db import models

# Create your models here.
from cvs.models import CV
from vacancies.models import Vacancy


class RelationStatus(models.Model):
    name = models.CharField(verbose_name='Название', null=False, max_length = 100)
    for_employer = models.BooleanField(verbose_name='Для работадателя')
    for_worker = models.BooleanField(verbose_name='Для соискателя')
    status_priority = models.IntegerField(verbose_name='Приоритет', null=False)


class Relations(models.Model):
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, db_index=True)
    cv = models.ForeignKey(CV, verbose_name='Резюме', on_delete=models.PROTECT)
    vacancy = models.ForeignKey(Vacancy, verbose_name='Вакансия', on_delete=models.PROTECT)

    class Meta:
        # Уникальный ключ на 2-е колонки.
        unique_together = ('cv', 'vacancy',)


class RelationHistory(models.Model):
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, db_index=True)
    relation = models.ForeignKey(Relations, verbose_name='Отношения', null=False, db_index=True, on_delete=models.CASCADE)
    status = models.ForeignKey(RelationStatus, verbose_name='Статус', null=False, db_index=True, on_delete=models.PROTECT)
    comment = models.TextField(verbose_name='Комментарий')
