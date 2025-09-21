#!/usr/bin/env python3
"""
Simple security test script for the Django Bookshelf application.

This script performs basic security checks to verify that the security
implementations are working correctly.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.conf import settings
from bookshelf.models import Book

User = get_user_model()


def test_security_settings():
    """Test that security settings are properly configured."""
    print("🔒 Testing Security Settings...")
    
    # Check that security settings are present
    security_settings = [
        'SECURE_BROWSER_XSS_FILTER',
        'SECURE_CONTENT_TYPE_NOSNIFF',
        'X_FRAME_OPTIONS',
        'CSRF_COOKIE_HTTPONLY',
        'SESSION_COOKIE_HTTPONLY',
        'SECURE_REFERRER_POLICY',
    ]
    
    for setting in security_settings:
        if hasattr(settings, setting):
            print(f"  ✅ {setting}: {getattr(settings, setting)}")
        else:
            print(f"  ❌ {setting}: Not configured")
    
    # Check CSP settings
    csp_settings = [
        'CSP_DEFAULT_SRC',
        'CSP_SCRIPT_SRC',
        'CSP_STYLE_SRC',
    ]
    
    print("\n🛡️ Content Security Policy Settings:")
    for setting in csp_settings:
        if hasattr(settings, setting):
            print(f"  ✅ {setting}: {getattr(settings, setting)}")
        else:
            print(f"  ❌ {setting}: Not configured")


def test_security_headers():
    """Test that security headers are present in responses."""
    print("\n🔒 Testing Security Headers...")
    
    client = Client()
    
    # Test the main bookshelf URL
    try:
        response = client.get('/bookshelf/')
        
        # Check for security headers
        headers_to_check = [
            ('X-Frame-Options', 'DENY'),
            ('X-Content-Type-Options', 'nosniff'),
            ('X-XSS-Protection', '1; mode=block'),
        ]
        
        for header, expected_value in headers_to_check:
            if header in response:
                actual_value = response[header]
                if actual_value == expected_value:
                    print(f"  ✅ {header}: {actual_value}")
                else:
                    print(f"  ⚠️ {header}: {actual_value} (expected: {expected_value})")
            else:
                print(f"  ❌ {header}: Not present")
                
    except Exception as e:
        print(f"  ❌ Error testing headers: {e}")


def test_csrf_protection():
    """Test that CSRF protection is working."""
    print("\n🔒 Testing CSRF Protection...")
    
    client = Client()
    
    # Try to make a POST request without CSRF token
    try:
        response = client.post('/bookshelf/add/', {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2023
        })
        
        if response.status_code == 403:
            print("  ✅ CSRF protection is working (403 Forbidden)")
        elif response.status_code == 200:
            print("  ⚠️ CSRF protection might not be working (200 OK)")
        else:
            print(f"  ❓ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Error testing CSRF: {e}")


def test_middleware_configuration():
    """Test that security middleware is properly configured."""
    print("\n🔒 Testing Middleware Configuration...")
    
    middleware = settings.MIDDLEWARE
    
    # Check for security-related middleware
    security_middleware = [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'bookshelf.middleware.SecurityHeadersMiddleware',
    ]
    
    for middleware_name in security_middleware:
        if middleware_name in middleware:
            print(f"  ✅ {middleware_name}: Configured")
        else:
            print(f"  ❌ {middleware_name}: Not configured")


def test_logging_configuration():
    """Test that security logging is configured."""
    print("\n🔒 Testing Logging Configuration...")
    
    if hasattr(settings, 'LOGGING'):
        logging_config = settings.LOGGING
        
        # Check for security loggers
        if 'loggers' in logging_config:
            security_loggers = ['django.security', 'django.request']
            
            for logger_name in security_loggers:
                if logger_name in logging_config['loggers']:
                    print(f"  ✅ Logger {logger_name}: Configured")
                else:
                    print(f"  ❌ Logger {logger_name}: Not configured")
        else:
            print("  ❌ No loggers configured")
    else:
        print("  ❌ No LOGGING configuration found")


def test_file_structure():
    """Test that security-related files exist."""
    print("\n🔒 Testing File Structure...")
    
    files_to_check = [
        'bookshelf/middleware.py',
        'SECURITY_IMPLEMENTATION.md',
        'bookshelf/security_tests.py',
    ]
    
    for file_path in files_to_check:
        full_path = project_dir / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}: Exists")
        else:
            print(f"  ❌ {file_path}: Missing")


def main():
    """Run all security tests."""
    print("🛡️ Django Bookshelf Security Test Suite")
    print("=" * 50)
    
    test_security_settings()
    test_middleware_configuration()
    test_logging_configuration()
    test_file_structure()
    test_security_headers()
    test_csrf_protection()
    
    print("\n" + "=" * 50)
    print("🔒 Security tests completed!")
    print("\nNote: Some tests may show warnings in development mode.")
    print("For production deployment, ensure all security settings are enabled.")


if __name__ == "__main__":
    main()
