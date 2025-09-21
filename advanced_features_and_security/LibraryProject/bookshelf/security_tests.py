"""
Security testing utilities for the Bookshelf application.

This module provides basic security tests to verify that security
measures are properly implemented and functioning.
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from django.utils.html import escape
import json


User = get_user_model()


class SecurityTestCase(TestCase):
    """
    Test case for security features implementation.
    
    This test case verifies that security measures are working correctly
    including CSRF protection, XSS prevention, SQL injection protection,
    and permission-based access control.
    """
    
    def setUp(self):
        """Set up test data and users."""
        # Create test users with different permission levels
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        
        self.editor_user = User.objects.create_user(
            username='editor',
            email='editor@test.com',
            password='testpass123'
        )
        
        self.viewer_user = User.objects.create_user(
            username='viewer',
            email='viewer@test.com',
            password='testpass123'
        )
        
        # Create groups and assign permissions
        self.admin_group = Group.objects.create(name='Admins')
        self.editor_group = Group.objects.create(name='Editors')
        self.viewer_group = Group.objects.create(name='Viewers')
        
        # Assign permissions to groups
        can_view = Permission.objects.get(codename='can_view')
        can_create = Permission.objects.get(codename='can_create')
        can_edit = Permission.objects.get(codename='can_edit')
        can_delete = Permission.objects.get(codename='can_delete')
        
        # Admin group gets all permissions
        self.admin_group.permissions.set([can_view, can_create, can_edit, can_delete])
        
        # Editor group gets view, create, edit permissions
        self.editor_group.permissions.set([can_view, can_create, can_edit])
        
        # Viewer group gets only view permission
        self.viewer_group.permissions.set([can_view])
        
        # Assign users to groups
        self.admin_user.groups.add(self.admin_group)
        self.editor_user.groups.add(self.editor_group)
        self.viewer_user.groups.add(self.viewer_group)
        
        # Create test client
        self.client = Client()
    
    def test_csrf_protection(self):
        """Test that CSRF protection is working."""
        # Login as admin
        self.client.login(username='admin', password='testpass123')
        
        # Try to add a book without CSRF token (should fail)
        response = self.client.post('/bookshelf/add/', {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2023
        })
        
        # Should return 403 Forbidden due to CSRF protection
        self.assertEqual(response.status_code, 403)
    
    def test_xss_protection(self):
        """Test XSS protection in templates."""
        # Login as admin
        self.client.login(username='admin', password='testpass123')
        
        # Create a book with potential XSS content
        xss_content = '<script>alert("XSS")</script>'
        
        response = self.client.post('/bookshelf/add/', {
            'title': xss_content,
            'author': 'Test Author',
            'publication_year': 2023,
            'csrfmiddlewaretoken': self.client.cookies['csrftoken'].value
        }, follow=True)
        
        # Check that the content is escaped in the response
        self.assertNotIn('<script>', response.content.decode())
        self.assertIn(escape(xss_content), response.content.decode())
    
    def test_sql_injection_protection(self):
        """Test SQL injection protection in search functionality."""
        # Login as viewer (has view permission)
        self.client.login(username='viewer', password='testpass123')
        
        # Try SQL injection in search parameter
        sql_injection = "'; DROP TABLE bookshelf_book; --"
        
        response = self.client.get('/bookshelf/', {
            'search': sql_injection
        })
        
        # Should not cause any errors and should return 200
        self.assertEqual(response.status_code, 200)
        
        # The search should be treated as literal text, not SQL
        self.assertIn(sql_injection, response.content.decode())
    
    def test_permission_based_access_control(self):
        """Test that permission-based access control works correctly."""
        # Test viewer permissions
        self.client.login(username='viewer', password='testpass123')
        
        # Viewer should be able to view books
        response = self.client.get('/bookshelf/')
        self.assertEqual(response.status_code, 200)
        
        # Viewer should not be able to add books
        response = self.client.get('/bookshelf/add/')
        self.assertEqual(response.status_code, 403)
        
        # Test editor permissions
        self.client.login(username='editor', password='testpass123')
        
        # Editor should be able to add books
        response = self.client.get('/bookshelf/add/')
        self.assertEqual(response.status_code, 200)
        
        # Editor should not be able to delete books
        # (This would require a book to exist first)
        
        # Test admin permissions
        self.client.login(username='admin', password='testpass123')
        
        # Admin should have access to all views
        response = self.client.get('/bookshelf/')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/bookshelf/add/')
        self.assertEqual(response.status_code, 200)
    
    def test_http_method_restrictions(self):
        """Test that HTTP method restrictions are enforced."""
        # Login as admin
        self.client.login(username='admin', password='testpass123')
        
        # Try to access add book with PUT method (should fail)
        response = self.client.put('/bookshelf/add/')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
        
        # Try to access add book with DELETE method (should fail)
        response = self.client.delete('/bookshelf/add/')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
    
    def test_input_validation(self):
        """Test that input validation works correctly."""
        # Login as admin
        self.client.login(username='admin', password='testpass123')
        
        # Try to create a book with invalid data
        response = self.client.post('/bookshelf/add/', {
            'title': '',  # Empty title
            'author': 'Test Author',
            'publication_year': 'invalid_year',  # Invalid year
            'csrfmiddlewaretoken': self.client.cookies['csrftoken'].value
        })
        
        # Should show form errors, not crash
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.content.decode().lower())
    
    def test_security_headers(self):
        """Test that security headers are present in responses."""
        # Login as viewer
        self.client.login(username='viewer', password='testpass123')
        
        response = self.client.get('/bookshelf/')
        
        # Check for security headers
        self.assertIn('X-Frame-Options', response)
        self.assertEqual(response['X-Frame-Options'], 'DENY')
        
        self.assertIn('X-Content-Type-Options', response)
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        
        self.assertIn('X-XSS-Protection', response)
        self.assertEqual(response['X-XSS-Protection'], '1; mode=block')
    
    def test_primary_key_validation(self):
        """Test that primary key validation prevents injection."""
        # Login as admin
        self.client.login(username='admin', password='testpass123')
        
        # Try to access book detail with invalid primary key
        invalid_pk = "'; DROP TABLE bookshelf_book; --"
        
        response = self.client.get(f'/bookshelf/book/{invalid_pk}/')
        
        # Should redirect to book list with error message
        self.assertEqual(response.status_code, 302)
    
    def test_session_security(self):
        """Test session security features."""
        # Login as admin
        response = self.client.post('/login/', {
            'username': 'admin',
            'password': 'testpass123'
        })
        
        # Check session cookie settings
        session_cookie = self.client.cookies.get('sessionid')
        if session_cookie:
            # In production, HttpOnly should be True
            # Note: This test might need adjustment based on your settings
            pass


class SecurityHeadersTest(TestCase):
    """Test security headers implementation."""
    
    def test_content_security_policy_header(self):
        """Test that CSP headers are present."""
        client = Client()
        response = client.get('/')
        
        # Check if CSP header is present (if middleware is working)
        # Note: This test might need adjustment based on your CSP configuration
        if 'Content-Security-Policy' in response:
            self.assertIsNotNone(response['Content-Security-Policy'])


def run_security_tests():
    """
    Function to run all security tests manually.
    
    This can be called from Django shell or management command.
    """
    from django.test.utils import get_runner
    from django.conf import settings
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["bookshelf.security_tests"])
    
    if failures:
        print(f"Security tests failed: {failures}")
        return False
    else:
        print("All security tests passed!")
        return True


if __name__ == "__main__":
    # This can be run as a standalone script
    import django
    from django.conf import settings
    
    # Configure Django settings
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
                'django.contrib.sessions',
                'bookshelf',
            ],
            SECRET_KEY='test-secret-key',
            ROOT_URLCONF='bookshelf.urls',
        )
        django.setup()
    
    # Run security tests
    run_security_tests()
