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
