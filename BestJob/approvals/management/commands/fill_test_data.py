import datetime

from django.core.management import BaseCommand
import json

from approvals.models import ApprovalStatus
from news.models import News

from users.models import User, EmployerProfile, WorkerProfile
from vacancies.models import Vacancy, Salary


JSON_PATH_NEWS = 'news/fixtures/'
JSON_PATH_USERS = 'users/fixtures/'
JSON_PATH_VACANCIES = 'vacancies/fixtures/'


def load_from_json(file_name):
    with open(file_name, mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):

        # Запуск после создания пользователя.
        news = load_from_json(JSON_PATH_NEWS + 'news.json')
        News.objects.all().delete()
        today = datetime.datetime.now(tz=datetime.timezone.utc)

        for n in news:
            j_news = n.get('fields')
            j_news['id'] = n.get('pk')
            author_id = j_news.get('author')
            author = User.objects.get(id=int(author_id))
            j_news['author'] = author
            j_news['created'] = today
            j_news['updated'] = today
            new_news = News(**j_news)
            new_news.save()

        employers = load_from_json(JSON_PATH_USERS + 'employers.json')
        EmployerProfile.objects.all().delete()

        for employer in employers:
            emp = employer.get('fields')
            emp['id'] = employer.get('pk')
            user = emp.get('user')
            _user = User.objects.get(id=user)
            emp['user'] = _user  # Заменяем юзера объектом

            status = emp.get('status')
            _status = ApprovalStatus.objects.get(id=status)
            emp['status'] = _status  # Заменяем юзера объектом

            new_employer = EmployerProfile(**emp)
            new_employer.save()

        # Соискатель
        workers = load_from_json(JSON_PATH_USERS + 'workers.json')
        WorkerProfile.objects.all().delete()

        for worker in workers:
            work = worker.get('fields')
            work['id'] = worker.get('pk')
            user = work.get('user')
            _user = User.objects.get(id=user)
            work['user'] = _user  # Заменяем юзера объектом

            new_worker = WorkerProfile(**work)
            new_worker.save()

        vacancies = load_from_json(JSON_PATH_VACANCIES + 'vacancies.json')
        Vacancy.objects.all().delete()

        for vacancy in vacancies:
            vac = vacancy.get('fields')
            vac['id'] = vacancy.get('pk')
            employer_profile = vac.get('employer_profile')
            _employer_profile = EmployerProfile.objects.get(id=employer_profile)
            vac['employer_profile'] = _employer_profile

            status = vac.get('status')
            _status = ApprovalStatus.objects.get(id=status)
            vac['status'] = _status

            new_vacancy = Vacancy(**vac)
            new_vacancy.save()

        salaries = load_from_json(JSON_PATH_VACANCIES + 'salaries.json')
        Salary.objects.all().delete()

        for salary in salaries:
            sal = salary.get('fields')
            sal['id'] = salary.get('pk')
            vacancy = sal.get('vacancy')
            _vacancy = Vacancy.objects.get(id=vacancy)
            sal['vacancy'] = _vacancy

            new_salary = Salary(**sal)
            new_salary.save()
