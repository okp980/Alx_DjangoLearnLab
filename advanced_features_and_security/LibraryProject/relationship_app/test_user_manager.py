"""
Test script to demonstrate the custom user manager functionality.
This file can be run independently to test the user manager methods.
"""

import os
import sys
import django
from datetime import date

# Add the project directory to Python path
sys.path.append('/Users/okpunoremmanuel/Documents/Engineering/ALX/Alx_DjangoLearnLab/advanced_features_and_security/LibraryProject')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import CustomUser, UserProfile


def test_create_user():
    """Test creating a regular user with custom fields."""
    print("Testing create_user method...")
    
    try:
        # Create a regular user
        user = CustomUser.objects.create_user(
            email='john.doe@example.com',
            username='johndoe',
            password='securepass123',
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1990, 5, 15)
        )
        
        print(f"✓ Successfully created user: {user.email}")
        print(f"  - Username: {user.username}")
        print(f"  - Date of Birth: {user.date_of_birth}")
        print(f"  - Is Staff: {user.is_staff}")
        print(f"  - Is Superuser: {user.is_superuser}")
        
        # Create user profile
        profile = UserProfile.objects.create(
            user=user,
            role='member'
        )
        print(f"✓ Created user profile with role: {profile.role}")
        
        return user
        
    except Exception as e:
        print(f"✗ Error creating user: {str(e)}")
        return None


def test_create_superuser():
    """Test creating a superuser with custom fields."""
    print("\nTesting create_superuser method...")
    
    try:
        # Create a superuser
        superuser = CustomUser.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123',
            first_name='Admin',
            last_name='User',
            date_of_birth=date(1985, 3, 10)
        )
        
        print(f"✓ Successfully created superuser: {superuser.email}")
        print(f"  - Username: {superuser.username}")
        print(f"  - Date of Birth: {superuser.date_of_birth}")
        print(f"  - Is Staff: {superuser.is_staff}")
        print(f"  - Is Superuser: {superuser.is_superuser}")
        
        return superuser
        
    except Exception as e:
        print(f"✗ Error creating superuser: {str(e)}")
        return None


def test_user_queries():
    """Test querying users with custom fields."""
    print("\nTesting user queries...")
    
    try:
        # Query all users
        all_users = CustomUser.objects.all()
        print(f"✓ Total users in database: {all_users.count()}")
        
        # Query users by email
        user_by_email = CustomUser.objects.filter(email__icontains='example.com')
        print(f"✓ Users with example.com email: {user_by_email.count()}")
        
        # Query users by date of birth
        users_born_1990 = CustomUser.objects.filter(date_of_birth__year=1990)
        print(f"✓ Users born in 1990: {users_born_1990.count()}")
        
        # Query superusers
        superusers = CustomUser.objects.filter(is_superuser=True)
        print(f"✓ Superusers: {superusers.count()}")
        
    except Exception as e:
        print(f"✗ Error querying users: {str(e)}")


def test_user_authentication():
    """Test user authentication with custom fields."""
    print("\nTesting user authentication...")
    
    try:
        from django.contrib.auth import authenticate
        
        # Test authentication with email
        user = authenticate(email='john.doe@example.com', password='securepass123')
        if user:
            print(f"✓ User authenticated successfully: {user.email}")
        else:
            print("✗ User authentication failed")
            
        # Test authentication with username
        user = authenticate(username='johndoe', password='securepass123')
        if user:
            print(f"✓ User authenticated with username: {user.username}")
        else:
            print("✗ Username authentication failed")
            
    except Exception as e:
        print(f"✗ Error during authentication: {str(e)}")


def cleanup_test_data():
    """Clean up test data."""
    print("\nCleaning up test data...")
    
    try:
        # Delete test users
        CustomUser.objects.filter(email__icontains='example.com').delete()
        print("✓ Test data cleaned up")
        
    except Exception as e:
        print(f"✗ Error cleaning up: {str(e)}")


if __name__ == '__main__':
    print("Custom User Manager Test Suite")
    print("=" * 40)
    
    # Run tests
    test_user = test_create_user()
    test_superuser = test_create_superuser()
    test_user_queries()
    test_user_authentication()
    
    # Ask if user wants to clean up
    cleanup = input("\nDo you want to clean up test data? (y/n): ")
    if cleanup.lower() == 'y':
        cleanup_test_data()
    
    print("\nTest suite completed!")
