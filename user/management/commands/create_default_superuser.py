# myapp/management/commands/create_default_superuser.py
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a default superuser with custom default values'

    def handle(self, *args, **options):
        # Check if the superuser already exists
        if not User.objects.filter(email='erfannasri2@gmail.com').exists():
            # Create the superuser with custom default values
            User.objects.create_superuser('erfannasri2@gmail.com', '123')

            self.stdout.write(self.style.SUCCESS('Successfully created default superuser'))
        else:
            self.stdout.write(self.style.SUCCESS('Default superuser already exists'))
