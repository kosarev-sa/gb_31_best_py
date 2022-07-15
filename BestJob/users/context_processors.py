import random

from BestJob.settings import UserRole
from users.models import WorkerProfile, EmployerProfile


def footer_lists(request):
    footer_employer_list = EmployerProfile.objects.all().exclude(
                status__status="NPB").exclude(status__status="RJC").exclude(image='')

    footer_data = {"footer_list_1": None, "footer_list_2": None }

    if footer_employer_list:
        if len(footer_employer_list) >= 6:
            footer_employer_list = random.sample(list(footer_employer_list), 6)
            footer_data["footer_list_1"] = footer_employer_list[0:3]
            footer_data["footer_list_2"] = footer_employer_list[3:]


    return footer_data


def roles(request):
    """добавляет значение ролей в контексте"""
    return {
        'roles': UserRole
    }
