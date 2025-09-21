from django.core.management.base import BaseCommand
from django.utils import timezone
from relationship_app.models import CustomUser, UserProfile
from datetime import date


class Command(BaseCommand):
    help = 'Demonstrates how to use the custom user manager to create users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email for the user',
            default='test@example.com'
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Username for the user',
            default='testuser'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the user',
            default='testpass123'
        )
        parser.add_argument(
            '--superuser',
            action='store_true',
            help='Create a superuser instead of regular user'
        )
        parser.add_argument(
            '--date-of-birth',
            type=str,
            help='Date of birth (YYYY-MM-DD)',
            default='1990-01-01'
        )

    def handle(self, *args, **options):
        email = options['email']
        username = options['username']
        password = options['password']
        is_superuser = options['superuser']
        date_of_birth = date.fromisoformat(options['date_of_birth'])

        try:
            if is_superuser:
                # Create superuser using custom manager
                user = CustomUser.objects.create_superuser(
                    email=email,
                    password=password,
                    username=username,
                    date_of_birth=date_of_birth,
                    first_name='Admin',
                    last_name='User'
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created superuser: {user.email}'
                    )
                )
            else:
                # Create regular user using custom manager
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    username=username,
                    date_of_birth=date_of_birth,
                    first_name='Regular',
                    last_name='User'
                )
                
                # Create user profile
                UserProfile.objects.create(
                    user=user,
                    role='member'
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created user: {user.email}'
                    )
                )

            # Display user information
            self.stdout.write(f'User ID: {user.id}')
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'Username: {user.username}')
            self.stdout.write(f'Date of Birth: {user.date_of_birth}')
            self.stdout.write(f'Is Staff: {user.is_staff}')
            self.stdout.write(f'Is Superuser: {user.is_superuser}')
            self.stdout.write(f'Is Active: {user.is_active}')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating user: {str(e)}')
            )
