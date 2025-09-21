from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from bookshelf.models import CustomUser

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test users and assign them to different groups for permission testing'

    def handle(self, *args, **options):
        # Test users data
        test_users = [
            {
                'username': 'viewer_user',
                'email': 'viewer@bookshelf.com',
                'password': 'testpass123',
                'group': 'Viewers',
            },
            {
                'username': 'editor_user',
                'email': 'editor@bookshelf.com',
                'password': 'testpass123',
                'group': 'Editors',
            },
            {
                'username': 'admin_user',
                'email': 'admin@bookshelf.com',
                'password': 'testpass123',
                'group': 'Admins',
            }
        ]
        
        for user_data in test_users:
            # Create or get user using CustomUser model
            user, created = CustomUser.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'is_active': True
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {user_data["username"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User already exists: {user_data["username"]}')
                )
            
            # Assign user to group
            try:
                group = Group.objects.get(name=user_data['group'])
                user.groups.add(group)
                self.stdout.write(f'  Assigned to group: {user_data["group"]}')
            except Group.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'  Group not found: {user_data["group"]}')
                )
            
            self.stdout.write('')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created/updated test users!')
        )
        self.stdout.write('\nTest users created:')
        self.stdout.write('  - viewer_user (password: testpass123) - Viewers group')
        self.stdout.write('  - editor_user (password: testpass123) - Editors group')
        self.stdout.write('  - admin_user (password: testpass123) - Admins group')
