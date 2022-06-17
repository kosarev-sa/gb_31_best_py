from django.db import models


# Create your models here.


class ApprovalStatus(models.Model):
    """model of status approval"""
    NOT_PUBLISHED = 'NPB'
    PUBLISHED = 'PUB'
    FOR_REVISION = 'FRV'
    REJECTED = 'RJC'
    APPROVED = 'APV'

    APPROVAL_STATUS_CHOICES = (
        (NOT_PUBLISHED, 'не опубликовано'),
        (PUBLISHED, 'опубликовано'),
        (FOR_REVISION, 'на доработку'),
        (REJECTED, 'отклонено'),
        (APPROVED, 'одобрено')
    )

    status = models.CharField(verbose_name='Статус', max_length=3, choices=APPROVAL_STATUS_CHOICES,
                              default=NOT_PUBLISHED, unique=True)

    def __str__(self):
        return self.status
