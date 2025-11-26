from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Reactivate a deactivated superuser account'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the superuser to reactivate')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            if user.is_active:
                self.stdout.write(
                    self.style.WARNING(f'User "{username}" is already active.')
                )
            else:
                user.is_active = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully reactivated user "{username}".')
                )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist.')
            )
