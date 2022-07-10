import random

from BestJob.settings import UserRole
from users.models import WorkerProfile, EmployerProfile


def footer_lists(request):
    footer_employer_list = EmployerProfile.objects.all()
    footer_employer_list = random.sample(list(footer_employer_list), 6)

    return {"footer_list_1": footer_employer_list[0:3],
            "footer_list_2": footer_employer_list[3:]
            }


def roles(request):
    """добавляет значение ролей в контексте"""
    return {
        'roles': UserRole
    }
