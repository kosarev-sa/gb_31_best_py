from django.db import models


# Create your models here.

class ApprovalStatus(models.Model):
    """model of status approval"""
    CHECKING = 'CHG'
    FOR_CORRECTION = 'COR'
    CANCELED = 'CNC'
    CHECKED = 'CHD'

    APPROVAL_STATUS_CHOISES = (
        (CHECKING, 'на проверке'),
        (FOR_CORRECTION, 'необходимо исправить'),
        (CANCELED, 'отклонение'),
        (CHECKED, 'проверено')
    )

    status = models.CharField(verbose_name='Статус', max_length=3, choices=APPROVAL_STATUS_CHOISES,
                              default=CHECKING, unique=True)

    def __str__(self):
        return self.status
