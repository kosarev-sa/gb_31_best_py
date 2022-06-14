from django.core.management.base import BaseCommand

from approvals.management.commands.fill_db import load_from_json
from users.models import User, Role
from news.models import News

JSON_PATH_ROLES = 'users/fixtures/'

class Command(BaseCommand):
    def handle(self, *args, **options):

        News.objects.all().delete()
        User.objects.all().delete()
        Role.objects.all().delete()

        superuser = User.objects.create_superuser('sirius', 'sirius@mail.ru', '1', pk=1)
        superuser.save()

        # Добавление ролей пользователей (Модератор, Работодатель, соискатель)
        roles = load_from_json(JSON_PATH_ROLES + 'roles.json')

        for role in roles:
            new_role = Role(pk=role['pk'],
                            role_name=role['role_name'])
            new_role.save()
            print(f'роль "{new_role}" была добавлена')

        role_id = 1
        for i in range(1, 6):

            if role_id > 3:
                role_id = 1

            user = User.objects.create_user(pk=i + 1, username=f'test_user_{i}', email=f'{i}@mail.ru', password=f'{i}',
                                            first_name=f'first_name_test_user_{i}', last_name=f'last_name_test_user_{i}',
                                            role_id=role_id)
            role_id += 1
            user.save()
