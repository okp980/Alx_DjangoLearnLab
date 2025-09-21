from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book, Author


class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **options):
        # Get content types for our models
        book_content_type = ContentType.objects.get_for_model(Book)
        author_content_type = ContentType.objects.get_for_model(Author)
        
        # Get all permissions for Book and Author models
        book_permissions = Permission.objects.filter(content_type=book_content_type)
        author_permissions = Permission.objects.filter(content_type=author_content_type)
        
        # Create Groups
        groups_data = {
            'Viewers': {
                'description': 'Users who can only view books and authors',
                'permissions': [
                    'relationship_app.can_view_book',
                    'relationship_app.can_view_author',
                ]
            },
            'Editors': {
                'description': 'Users who can view, create, and edit books and authors',
                'permissions': [
                    'relationship_app.can_view_book',
                    'relationship_app.can_create_book',
                    'relationship_app.can_edit_book',
                    'relationship_app.can_view_author',
                    'relationship_app.can_create_author',
                    'relationship_app.can_edit_author',
                ]
            },
            'Admins': {
                'description': 'Users who have full access including delete permissions',
                'permissions': [
                    'relationship_app.can_view_book',
                    'relationship_app.can_create_book',
                    'relationship_app.can_edit_book',
                    'relationship_app.can_delete_book',
                    'relationship_app.can_view_author',
                    'relationship_app.can_create_author',
                    'relationship_app.can_edit_author',
                    'relationship_app.can_delete_author',
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
