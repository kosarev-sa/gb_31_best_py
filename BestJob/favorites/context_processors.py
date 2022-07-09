from django import template

from cvs.models import CV
from favorites.models import WorkerFavorites, EmployerFavorites
from users.models import WorkerProfile, EmployerProfile
from vacancies.models import Vacancy

register = template.Library()


@register.simple_tag()
def is_workers_favorite(vacancy_id, worker_id):
    worker = WorkerProfile.objects.get(id=worker_id)
    vacancy = Vacancy.objects.get(id=vacancy_id)
    wf = WorkerFavorites.objects.filter(worker_profile=worker.id, vacancy=vacancy.id)
    if wf:
        return True
    else:
        return False

@register.simple_tag()
def is_employers_favorite(cv_id, employer_id):
    employer = EmployerProfile.objects.get(id=employer_id)
    cv = CV.objects.get(id=cv_id)
    ef = EmployerFavorites.objects.filter(employer_profile=employer.id, cv=cv.id)
    if ef:
        return True
    else:
        return False

