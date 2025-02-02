import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@localhost.ru',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

        user.set_password(os.getenv('SUPERUSER_PASSWORD'))
        user.save()