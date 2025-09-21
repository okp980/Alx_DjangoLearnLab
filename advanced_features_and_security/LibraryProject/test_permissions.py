#!/usr/bin/env python
"""
Test script to demonstrate the permission system.
Run this script to test permissions programmatically.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book, Author, UserProfile


def test_permissions():
    """Test the permission system by checking user permissions."""
    
    print("=== Testing Django Custom Permissions System ===\n")
    
    # Test users
    test_users = ['viewer_user', 'editor_user', 'admin_user']
    
    for username in test_users:
        try:
            user = User.objects.get(username=username)
            print(f"Testing user: {username}")
            print(f"  Email: {user.email}")
            print(f"  Groups: {[group.name for group in user.groups.all()]}")
            
            # Check permissions
            permissions = {
                'can_view_book': user.has_perm('relationship_app.can_view'),
                'can_create_book': user.has_perm('relationship_app.can_create'),
                'can_edit_book': user.has_perm('relationship_app.can_edit'),
                'can_delete_book': user.has_perm('relationship_app.can_delete'),
            }
            
            print("  Permissions:")
            for perm_name, has_perm in permissions.items():
                status = "✓" if has_perm else "✗"
                print(f"    {status} {perm_name}")
            
            # Check user profile role
            try:
                profile = UserProfile.objects.get(user=user)
                print(f"  Role: {profile.role}")
            except UserProfile.DoesNotExist:
                print("  Role: No profile found")
            
            print()
            
        except User.DoesNotExist:
            print(f"User {username} not found. Run 'python manage.py create_test_users' first.\n")
    
    # Test groups and their permissions
    print("=== Group Permissions ===\n")
    
    groups = ['Viewers', 'Editors', 'Admins']
    for group_name in groups:
        try:
            group = Group.objects.get(name=group_name)
            print(f"Group: {group_name}")
            print(f"  Permissions:")
            for perm in group.permissions.all():
                print(f"    - {perm.codename}: {perm.name}")
            print()
        except Group.DoesNotExist:
            print(f"Group {group_name} not found. Run 'python manage.py setup_groups' first.\n")
    
    # Test model permissions
    print("=== Model Permissions ===\n")
    
    book_content_type = ContentType.objects.get_for_model(Book)
    author_content_type = ContentType.objects.get_for_model(Author)
    
    book_permissions = Permission.objects.filter(content_type=book_content_type)
    author_permissions = Permission.objects.filter(content_type=author_content_type)
    
    print("Book Model Permissions:")
    for perm in book_permissions:
        print(f"  - {perm.codename}: {perm.name}")
    
    print("\nAuthor Model Permissions:")
    for perm in author_permissions:
        print(f"  - {perm.codename}: {perm.name}")
    
    print("\n=== Test Complete ===")


if __name__ == '__main__':
    test_permissions()
