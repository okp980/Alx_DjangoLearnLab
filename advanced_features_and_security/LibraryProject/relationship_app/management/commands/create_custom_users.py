"""
Management command to create custom users for testing purposes.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Create custom users for testing'

    def handle(self, *args, **options):
        # Create a regular user
        user_data = {
            'email': 'user@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': date(1990, 5, 15),
        }
        
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults=user_data
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created user: {user.email}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'User already exists: {user.email}')
            )
        
        # Create a superuser
        superuser_data = {
            'email': 'admin@example.com',
            'username': 'admin',
            'first_name': 'Admin',
            'last_name': 'User',
            'date_of_birth': date(1985, 3, 20),
        }
        
        superuser, created = User.objects.get_or_create(
            email=superuser_data['email'],
            defaults=superuser_data
        )
        
        if created:
            superuser.set_password('adminpass123')
            superuser.is_staff = True
            superuser.is_superuser = True
            superuser.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser: {superuser.email}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Superuser already exists: {superuser.email}')
            )