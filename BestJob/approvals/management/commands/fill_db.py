from django.core.management import BaseCommand

from users.models import Role


class Command(BaseCommand):
    def handle(self, *args, **options):

        print('hello')