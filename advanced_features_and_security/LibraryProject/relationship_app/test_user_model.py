"""
Test file for the custom user model implementation.
Run this to verify the custom user model works correctly.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date

User = get_user_model()

class CustomUserModelTest(TestCase):
    """Test cases for the CustomUser model."""
    
    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': date(1990, 5, 15),
        }
    
    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            password='testpass123',
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            date_of_birth=self.user_data['date_of_birth']
        )
        
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.date_of_birth, self.user_data['date_of_birth'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password('testpass123'))
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.check_password('adminpass123'))
    
    def test_email_uniqueness(self):
        """Test that email field is unique."""
        User.objects.create_user(
            email='unique@example.com',
            username='user1',
            password='testpass123'
        )
        
        with self.assertRaises(Exception):  # Should raise IntegrityError
            User.objects.create_user(
                email='unique@example.com',
                username='user2',
                password='testpass123'
            )
    
    def test_user_str_representation(self):
        """Test the string representation of the user."""
        user = User.objects.create_user(
            email='str@example.com',
            username='struser',
            password='testpass123'
        )
        
        self.assertEqual(str(user), 'str@example.com')
    
    def test_optional_fields(self):
        """Test that optional fields can be null."""
        user = User.objects.create_user(
            email='optional@example.com',
            username='optuser',
            password='testpass123'
        )
        
        self.assertIsNone(user.date_of_birth)
        self.assertFalse(bool(user.profile_photo))
    
    def test_username_field_setting(self):
        """Test that email is set as USERNAME_FIELD."""
        self.assertEqual(User.USERNAME_FIELD, 'email')
        self.assertEqual(User.REQUIRED_FIELDS, ['username'])

if __name__ == '__main__':
    # Run the tests
    import django
    from django.conf import settings
    from django.test.utils import get_runner
    
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'relationship_app',
            ],
            AUTH_USER_MODEL='relationship_app.CustomUser',
            USE_TZ=True,
        )
        django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['relationship_app.test_user_model'])
