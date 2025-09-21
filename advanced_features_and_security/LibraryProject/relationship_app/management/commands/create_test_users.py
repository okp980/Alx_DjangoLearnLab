from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from relationship_app.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test users and assign them to different groups for permission testing'

    def handle(self, *args, **options):
        # Test users data
        test_users = [
            {
                'username': 'viewer_user',
                'email': 'viewer@example.com',
                'password': 'testpass123',
                'group': 'Viewers',
                'role': 'member'
            },
            {
                'username': 'editor_user',
                'email': 'editor@example.com',
                'password': 'testpass123',
                'group': 'Editors',
                'role': 'librarian'
            },
            {
                'username': 'admin_user',
                'email': 'admin@example.com',
                'password': 'testpass123',
                'group': 'Admins',
                'role': 'admin'
            }
        ]
        
        for user_data in test_users:
            # Create or get user
            user, created = User.objects.get_or_create(
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
            
            # Create or update user profile
            user_profile, profile_created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': user_data['role']}
            )
            
            if profile_created:
                self.stdout.write(f'  Created profile with role: {user_data["role"]}')
            else:
                user_profile.role = user_data['role']
                user_profile.save()
                self.stdout.write(f'  Updated profile role to: {user_data["role"]}')
            
            self.stdout.write('')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created/updated test users!')
        )
        self.stdout.write('\nTest users created:')
        self.stdout.write('  - viewer_user (password: testpass123) - Viewers group')
        self.stdout.write('  - editor_user (password: testpass123) - Editors group')
        self.stdout.write('  - admin_user (password: testpass123) - Admins group')
