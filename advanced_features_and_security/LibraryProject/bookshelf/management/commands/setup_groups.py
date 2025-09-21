from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Create user groups and assign permissions for bookshelf app'

    def handle(self, *args, **options):
        # Get content type for Book model
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get all permissions for Book model
        book_permissions = Permission.objects.filter(content_type=book_content_type)
        
        # Create Groups
        groups_data = {
            'Viewers': {
                'description': 'Users who can only view books',
                'permissions': [
                    'bookshelf.can_view',
                ]
            },
            'Editors': {
                'description': 'Users who can view, create, and edit books',
                'permissions': [
                    'bookshelf.can_view',
                    'bookshelf.can_create',
                    'bookshelf.can_edit',
                ]
            },
            'Admins': {
                'description': 'Users who have full access including delete permissions',
                'permissions': [
                    'bookshelf.can_view',
                    'bookshelf.can_create',
                    'bookshelf.can_edit',
                    'bookshelf.can_delete',
                ]
            }
        }
        
        # Create groups and assign permissions
        for group_name, group_info in groups_data.items():
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created group: {group_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Group already exists: {group_name}')
                )
            
            # Clear existing permissions and add new ones
            group.permissions.clear()
            
            # Add permissions to the group
            for perm_codename in group_info['permissions']:
                try:
                    permission = Permission.objects.get(codename=perm_codename.split('.')[-1])
                    group.permissions.add(permission)
                    self.stdout.write(f'  Added permission: {perm_codename}')
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'  Permission not found: {perm_codename}')
                    )
            
            self.stdout.write(f'  Description: {group_info["description"]}')
            self.stdout.write('')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up all groups and permissions!')
        )
