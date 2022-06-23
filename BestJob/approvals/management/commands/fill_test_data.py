import datetime

from django.core.management import BaseCommand
import json

from approvals.models import ApprovalStatus
from news.models import News
from users.models import User, EmployerProfile, WorkerProfile, ModeratorProfile

from vacancies.models import Vacancy
from cvs.models import CV, CVSkills, CVEmployment, CVWorkSchedule, Education, Experience, LanguagesSpoken, \
    ConnectVacancyCv
from search.models import Category, MainSkills, Languages, LanguageLevels, Employments, WorkSchedules

JSON_PATH_NEWS = 'news/fixtures/'
JSON_PATH_USERS = 'users/fixtures/'
JSON_PATH_VACANCIES = 'vacancies/fixtures/'
JSON_PATH_CV = 'cvs/fixtures/'


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

            birth_date = datetime.datetime.strptime(work.get('birth_date'), '%Y-%m-%d')
            birth_date = birth_date.replace(tzinfo=datetime.timezone.utc)
            work['birth_date'] = birth_date

            new_worker = WorkerProfile(**work)
            new_worker.save()

        moderators = load_from_json(JSON_PATH_USERS + 'moderator.json')
        ModeratorProfile.objects.all().delete()

        for moderator in moderators:
            moder = moderator.get('fields')
            moder['id'] = moderator.get('pk')
            user_id = moder.get('user')
            _user = User.objects.get(id=user_id)
            moder['user'] = _user  # Заменяем юзера объектом

            date_create = datetime.datetime.strptime(moder.get('date_create'), '%Y-%m-%dT%H:%M:%S')
            date_create = date_create.replace(tzinfo=datetime.timezone.utc)
            moder['date_create'] = date_create

            new_moder = ModeratorProfile(**moder)
            new_moder.save()

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

            specialization = vac.get('specialization')
            _specialization = Category.objects.get(code=specialization)
            vac['specialization'] = _specialization

            new_vacancy = Vacancy(**vac)
            new_vacancy.save()

        cvs = load_from_json(JSON_PATH_CV + 'cv.json')
        CV.objects.all().delete()

        for cv in cvs:
            cv_row = cv.get('fields')
            cv_row['id'] = cv.get('pk')

            worker_profile = cv_row.get('worker_profile')
            _worker_profile = WorkerProfile.objects.get(id=worker_profile)
            cv_row['worker_profile'] = _worker_profile

            status = cv_row.get('status')
            _status = ApprovalStatus.objects.get(id=status)
            cv_row['status'] = _status

            speciality = cv_row.get('speciality')
            _speciality = Category.objects.get(code=speciality)
            cv_row['speciality'] = _speciality

            new_cv = CV(**cv_row)
            new_cv.save()

        cv_skills = load_from_json(JSON_PATH_CV + 'cv_skills.json')
        CVSkills.objects.all().delete()

        for skill in cv_skills:
            j_skill = {}
            cv_id = skill.get('cv')
            _cv = CV.objects.get(id=cv_id)
            j_skill['cv'] = _cv

            skill_code = skill.get('skill')
            _skill = MainSkills.objects.get(code=skill_code)
            j_skill['skill'] = _skill

            new_cv_skill = CVSkills(**j_skill)
            new_cv_skill.save()

        cv_educations = load_from_json(JSON_PATH_CV + 'cv_education.json')
        Education.objects.all().delete()

        for educ in cv_educations:
            ed_row = {}
            ed_row = educ
            cv_id = educ.get('cv')
            _cv = CV.objects.get(id=cv_id)
            ed_row['cv'] = _cv
            new_education = Education(**ed_row)
            new_education.save()

        experiences = load_from_json(JSON_PATH_CV + 'cv_experiences.json')
        Experience.objects.all().delete()

        for exp in experiences:
            exp_row = {}
            exp_row = exp
            cv_id = exp.get('cv')
            _cv = CV.objects.get(id=cv_id)
            exp_row['cv'] = _cv

            new_experience = Experience(**exp_row)
            new_experience.save()

        languages = load_from_json(JSON_PATH_CV + 'сv_languages.json')
        LanguagesSpoken.objects.all().delete()

        for lan in languages:
            lan_row = {}

            cv_id = lan.get('cv')
            _cv = CV.objects.get(id=cv_id)
            lan_row['cv'] = _cv

            lan_code = lan.get('language')
            _lan = Languages.objects.get(code=lan_code)
            lan_row["language"] = _lan

            lev_code = lan.get('level')
            _lev = LanguageLevels.objects.get(code=lev_code)
            lan_row['level'] = _lev

            new_language = LanguagesSpoken(**lan_row)
            new_language.save()

        employments = load_from_json(JSON_PATH_CV + 'cv_employments.json')
        CVEmployment.objects.all().delete()

        for emp in employments:
            emp_row = {}

            cv_id = emp.get('cv')
            _cv = CV.objects.get(id=cv_id)
            emp_row['cv'] = _cv

            emp_code = emp.get('employment')
            _emp = Employments.objects.get(code=emp_code)
            emp_row['employment'] = _emp

            new_employment = CVEmployment(**emp_row)
            new_employment.save()

        schedules = load_from_json(JSON_PATH_CV + 'cv_shedules.json')
        CVWorkSchedule.objects.all().delete()

        for sched in schedules:
            sch_row = {}

            cv_id = sched.get('cv')
            _cv = CV.objects.get(id=cv_id)
            sch_row['cv'] = _cv

            sch_code = sched.get('schedule')
            _sch = WorkSchedules.objects.get(code=sch_code)
            sch_row['schedule'] = _sch

            new_schedule = CVWorkSchedule(**sch_row)
            new_schedule.save()

        cv_responses = load_from_json(JSON_PATH_CV + 'cv_responses.json')
        ConnectVacancyCv.objects.all().delete()

        for resp in cv_responses:
            resp['cv'] = CV.objects.get(id=resp['cv'])
            resp['vacancy'] = Vacancy.objects.get(id=resp['vacancy'])
            ConnectVacancyCv(**resp).save()
