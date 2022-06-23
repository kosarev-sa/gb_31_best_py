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

    def get_status_name(self, key):
        for status in self.APPROVAL_STATUS_CHOICES:
            if status[0] == key:
                return status[1]

    def get_status_code(self, key):
        for status in self.APPROVAL_STATUS_CHOICES:
            if status[0] == key:
                return status[0]

    def __str__(self):
        return self.get_status_name(self.status)

    def code(self):
        return self.get_status_code(self.status)