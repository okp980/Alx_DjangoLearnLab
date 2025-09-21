# Custom User Model Implementation

This document outlines the implementation of a custom user model in the Django project, extending the built-in `AbstractUser` model with additional fields and functionality.

## Overview

The custom user model (`CustomUser`) extends Django's `AbstractUser` to include:

- **date_of_birth**: A date field for storing user's birth date
- **profile_photo**: An image field for storing user profile pictures
- **email as username**: Email is used as the primary identifier instead of username

## Implementation Details

### 1. Custom User Model (`models.py`)

```python
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
```

**Key Features:**

- Email field is unique and used as the primary identifier
- Date of birth field allows null values for flexibility
- Profile photo field with automatic upload to 'profile_photos/' directory
- Custom user manager handles user creation and management

### 2. Custom User Manager

The `CustomUserManager` extends `BaseUserManager` and implements:

- **`create_user(email, password=None, **extra_fields)`\*\*: Creates regular users
- **`create_superuser(email, password=None, **extra_fields)`\*\*: Creates admin users

Both methods properly handle the email-based authentication system.

### 3. Settings Configuration (`settings.py`)

```python
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

The `AUTH_USER_MODEL` setting tells Django to use our custom user model instead of the default User model.

### 4. Admin Interface (`admin.py`)

The custom admin interface includes:

- **Profile photo preview**: Shows thumbnail images in the user list
- **Organized fieldsets**: Groups related fields logically
- **Search and filtering**: Email, username, and name-based search
- **Custom add forms**: Streamlined user creation process

### 5. URL Configuration

Media file serving is configured for development:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Usage Examples

### Creating Users Programmatically

```python
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

# Create a regular user
user = User.objects.create_user(
    email='john@example.com',
    username='john_doe',
    password='secure_password',
    first_name='John',
    last_name='Doe',
    date_of_birth=date(1990, 5, 15)
)

# Create a superuser
admin = User.objects.create_superuser(
    email='admin@example.com',
    username='admin',
    password='admin_password'
)
```

### Using the Management Command

```bash
python manage.py create_custom_users
```

This command creates test users for development and testing purposes.

### Accessing User Data

```python
# Get user by email (primary identifier)
user = User.objects.get(email='john@example.com')

# Access custom fields
print(user.date_of_birth)
print(user.profile_photo)

# Check if user has a profile photo
if user.profile_photo:
    print(f"Profile photo URL: {user.profile_photo.url}")
```

## Database Migration

When implementing a custom user model:

1. **Create migrations**: `python manage.py makemigrations`
2. **Apply migrations**: `python manage.py migrate`
3. **Handle existing data**: If migrating from default User model, data migration may be required

## Security Considerations

1. **Email validation**: The email field is automatically validated
2. **Password handling**: Uses Django's built-in password hashing
3. **File uploads**: Profile photos are stored securely with proper validation
4. **Admin permissions**: Proper permission handling for staff and superuser accounts

## File Structure

```
bookshelf/
├── models.py              # Custom user model and manager
├── admin.py               # Admin interface configuration
├── management/
│   └── commands/
│       └── create_custom_users.py  # Management command
└── ...

LibraryProject/
├── settings.py            # AUTH_USER_MODEL configuration
└── urls.py               # Media file serving
```

## Testing

The implementation includes:

- Management command for creating test users
- Admin interface testing capabilities
- Proper field validation and constraints

## Next Steps

1. Run migrations to apply the custom user model
2. Test user creation and authentication
3. Verify admin interface functionality
4. Test profile photo upload and display
5. Update any existing views or forms to use the custom user model

## Troubleshooting

**Common Issues:**

- **Migration conflicts**: Ensure all migrations are applied in order
- **Admin access**: Use email instead of username for login
- **Media files**: Check MEDIA_URL and MEDIA_ROOT settings
- **Foreign key references**: Update any models referencing the old User model
