import datetime
from django.core.management.base import BaseCommand

from BestJob.settings import UserRole
from approvals.models import ApprovalStatus
from approvals.management.commands.fill_db import load_from_json
from users.models import User, Role, EmployerProfile, WorkerProfile, ModeratorProfile
from news.models import News

JSON_PATH_USERS = 'users/fixtures/'


class Command(BaseCommand):
    user_pk = 0
    ROLES_MAP = {
        'moderator': UserRole.MODERATOR,
        'employer': UserRole.EMPLOYER,
        'worker': UserRole.WORKER
    }

    def create_user(self, role):
        self.user_pk += 1
        print(f'Создан пользователь {role}_{self.user_pk}\tПароль {self.user_pk}')
        user = User.objects.create_user(pk=self.user_pk, username=f'{role}_{self.user_pk}',
                                        email=f'{self.user_pk}@mail.ru', password=f'{self.user_pk}',
                                        first_name=f'first_name_{self.user_pk}', last_name=f'last_name_{self.user_pk}',
                                        role_id=self.ROLES_MAP[role])
        user.save()
        return self.user_pk

    def handle(self, *args, **options):

        News.objects.all().delete()
        User.objects.all().delete()
        Role.objects.all().delete()

        superuser = User.objects.create_superuser('sirius', 'sirius@mail.ru', '1', pk=1)
        superuser.save()

        # Добавление ролей пользователей (Модератор, Работодатель, соискатель)
        roles = load_from_json(JSON_PATH_USERS + 'roles.json')

        for role in roles:
            new_role = Role(pk=role['pk'],
                            role_name=role['role_name'])
            new_role.save()
            print(f'роль "{new_role}" была добавлена')

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
