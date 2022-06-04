from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        superuser = User.objects.create_superuser('sirius', 'sirius@mail.ru', '1')
        superuser.save()

        for i in range(1, 6):
            user = User.objects.create_user(username=f'test_user_{i}', email=f'{i}@mail.ru', password=f'{i}',
                                            first_name=f'first_name_test_user_{i}', last_name=f'last_name_test_user_{i}')
            user.save()
