import datetime

from django.core.management import BaseCommand
import json

from approvals.models import ApprovalStatus
from favorites.models import EmployerFavorites, WorkerFavorites
from news.models import News
from relations.models import Relations, RelationHistory, RelationStatus
from users.models import User, EmployerProfile, WorkerProfile, ModeratorProfile

from vacancies.models import Vacancy
from cvs.models import CV, CVSkills, CVEmployment, CVWorkSchedule, Education, Experience, LanguagesSpoken, \
    ConnectVacancyCv
from search.models import Category, MainSkills, Languages, LanguageLevels, Employments, WorkSchedules

JSON_PATH_NEWS = 'news/fixtures/'
JSON_PATH_USERS = 'users/fixtures/'
JSON_PATH_VACANCIES = 'vacancies/fixtures/'
JSON_PATH_CV = 'cvs/fixtures/'
JSON_PATH_RELATIONS = 'relations/fixtures/'
JSON_PATH_FAVORITES = 'favorites/fixtures/'


def load_from_json(file_name):
    with open(file_name, mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    user_pk = 0
    ROLES_MAP = {
        'moderator': 1,
        'employer': 2,
        'worker': 3
    }

    def create_user(self, role):
        self.user_pk += 1
        print(f'Создан пользовател {role}_{self.user_pk}\tПароль {self.user_pk}')
        user = User.objects.create_user(pk=self.user_pk, username=f'{role}_{self.user_pk}',
                                        email=f'{self.user_pk}@mail.ru', password=f'{self.user_pk}',
                                        first_name=f'first_name_{self.user_pk}', last_name=f'last_name_{self.user_pk}',
                                        role_id=self.ROLES_MAP[role])
        user.save()
        return self.user_pk

    def handle(self, *args, **options):

        RelationHistory.objects.all().delete()
        Relations.objects.all().delete()
        EmployerFavorites.objects.all().delete()
        WorkerFavorites.objects.all().delete()

        moderators = load_from_json(JSON_PATH_USERS + 'moderator.json')
        ModeratorProfile.objects.all().delete()

        for moderator in moderators:
            user_id = self.create_user('moderator')
            moderator['id'] = user_id
            moderator['user'] = User.objects.get(id=user_id)  # Заменяем юзера объектом

            date_create = datetime.datetime.strptime(moderator.get('date_create'), '%Y-%m-%dT%H:%M:%S')
            date_create = date_create.replace(tzinfo=datetime.timezone.utc)
            moderator['date_create'] = date_create

            new_moder = ModeratorProfile(**moderator)
            new_moder.save()

        employers = load_from_json(JSON_PATH_USERS + 'employers.json')
        EmployerProfile.objects.all().delete()

        for employer in employers:
            user_id = self.create_user('employer')
            employer['id'] = user_id
            employer['user'] = User.objects.get(id=user_id)  # Заменяем юзера объектом

            status = employer.get('status')
            employer['status'] = ApprovalStatus.objects.get(id=status)  # Заменяем юзера объектом
            new_employer = EmployerProfile(**employer)
            new_employer.save()

        # Соискатель
        workers = load_from_json(JSON_PATH_USERS + 'workers.json')
        WorkerProfile.objects.all().delete()

        for worker in workers:
            user_id = self.create_user('worker')
            worker['id'] = user_id
            worker['user'] = User.objects.get(id=user_id)  # Заменяем юзера объектом

            birth_date = datetime.datetime.strptime(worker.get('birth_date'), '%Y-%m-%d')
            birth_date = birth_date.replace(tzinfo=datetime.timezone.utc)
            worker['birth_date'] = birth_date

            new_worker = WorkerProfile(**worker)
            new_worker.save()

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

        # RELATIONS
        relations = load_from_json(JSON_PATH_RELATIONS + 'relation.json')

        for relation in relations:
            relation_row = relation.get('fields')
            relation_row['id'] = relation.get('pk')

            date_create = datetime.datetime.strptime(relation_row.get('created'), '%Y-%m-%dT%H:%M:%S')
            date_create = date_create.replace(tzinfo=datetime.timezone.utc)
            relation_row['created'] = date_create

            relation_row['cv'] = CV.objects.get(id=relation_row['cv'])
            relation_row['vacancy'] = Vacancy.objects.get(id=relation_row['vacancy'])

            new_relation = Relations(**relation_row)
            new_relation.save()

        relations_history = load_from_json(JSON_PATH_RELATIONS + 'relation_history.json')

        for rh in relations_history:
            rh_row = rh.get('fields')
            rh_row['id'] = rh.get('pk')

            date_create = datetime.datetime.strptime(rh_row.get('created'), '%Y-%m-%dT%H:%M:%S')
            date_create = date_create.replace(tzinfo=datetime.timezone.utc)
            rh_row['created'] = date_create

            rh_row['relation'] = Relations.objects.get(pk=rh_row['relation'])
            rh_row['status'] = RelationStatus.objects.get(pk=rh_row['status'])

            new_rh = RelationHistory(**rh_row)
            new_rh.save()

        # JSON_PATH_FAVORITES
        employer_favorites = load_from_json(JSON_PATH_FAVORITES + 'employerfavorites.json')

        for emp_fav in employer_favorites:
            emp_fav_row = emp_fav.get('fields')
            emp_fav_row['id'] = emp_fav.get('pk')
            emp_fav_row['cv'] = CV.objects.get(id=emp_fav_row['cv'])
            emp_fav_row['employer_profile'] = EmployerProfile.objects.get(id=emp_fav_row['employer_profile'])
            EmployerFavorites(**emp_fav_row).save()

        worker_favorites = load_from_json(JSON_PATH_FAVORITES + 'workerfavorites.json')

        for work_fav in worker_favorites:
            work_fav_row = work_fav.get('fields')
            work_fav_row['id'] = work_fav.get('pk')
            work_fav_row['vacancy'] = Vacancy.objects.get(id=work_fav_row['vacancy'])
            work_fav_row['worker_profile'] = WorkerProfile.objects.get(id=work_fav_row['worker_profile'])
            WorkerFavorites(**work_fav_row).save()
