# Django Custom Permissions and Groups Setup

This document explains the custom permissions and user groups implementation in the Library Project.

## Overview

The application implements a comprehensive permission system with custom permissions and user groups to control access to different actions on Book and Author models.

## Custom Permissions

### Models with Custom Permissions

#### Book Model (`relationship_app/models.py`)

```python
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
        )
```

#### Author Model (`relationship_app/models.py`)

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (
            ('can_view', 'Can view author'),
            ('can_create', 'Can create author'),
            ('can_edit', 'Can edit author'),
            ('can_delete', 'Can delete author'),
        )
```

## User Groups

The system defines three main user groups with different permission levels:

### 1. Viewers Group

- **Permissions**: `can_view` for both Book and Author models
- **Description**: Users who can only view books and authors
- **Use Case**: Regular library members who can browse the catalog

### 2. Editors Group

- **Permissions**: `can_view`, `can_create`, `can_edit` for both Book and Author models
- **Description**: Users who can view, create, and edit books and authors
- **Use Case**: Librarians who manage the library catalog

### 3. Admins Group

- **Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete` for both Book and Author models
- **Description**: Users who have full access including delete permissions
- **Use Case**: System administrators with complete control

## Permission Enforcement in Views

All views are protected using Django's `@permission_required` decorator with `raise_exception=True`:

### Book Views

```python
@permission_required('relationship_app.can_view', raise_exception=True)
def list_books(request):
    # View books

@permission_required('relationship_app.can_create', raise_exception=True)
def add_book(request):
    # Create new book

@permission_required('relationship_app.can_edit', raise_exception=True)
def change_book(request, pk):
    # Edit existing book

@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    # Delete book
```

### Author Views

```python
@permission_required('relationship_app.can_view', raise_exception=True)
def list_authors(request):
    # View authors

@permission_required('relationship_app.can_create', raise_exception=True)
def add_author(request):
    # Create new author

@permission_required('relationship_app.can_edit', raise_exception=True)
def change_author(request, pk):
    # Edit existing author

@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_author(request, pk):
    # Delete author
```

## Setup Commands

### 1. Create Groups and Assign Permissions

```bash
python manage.py setup_groups
```

This command creates the three user groups and assigns the appropriate permissions to each group.

### 2. Create Test Users

```bash
python manage.py create_test_users
```

This command creates test users for each group:

- `viewer_user` (password: testpass123) - Viewers group
- `editor_user` (password: testpass123) - Editors group
- `admin_user` (password: testpass123) - Admins group

## Testing the Permission System

### Manual Testing Steps

1. **Run the setup commands**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py setup_groups
   python manage.py create_test_users
   ```

2. **Test Viewer User**:

   - Login as `viewer_user`
   - Should be able to view books and authors
   - Should get 403 Forbidden when trying to create/edit/delete

3. **Test Editor User**:

   - Login as `editor_user`
   - Should be able to view, create, and edit books and authors
   - Should get 403 Forbidden when trying to delete

4. **Test Admin User**:
   - Login as `admin_user`
   - Should have full access to all operations

### URL Endpoints for Testing

- Books: `/relationship_app/books/`
- Add Book: `/relationship_app/add_book/`
- Edit Book: `/relationship_app/edit_book/<id>/`
- Delete Book: `/relationship_app/delete_book/<id>/`
- Authors: `/relationship_app/authors/`
- Add Author: `/relationship_app/add_author/`
- Edit Author: `/relationship_app/edit_author/<id>/`
- Delete Author: `/relationship_app/delete_author/<id>/`

## Permission Checking in Templates

You can also check permissions in templates using the `perms` template variable:

```html
{% if perms.relationship_app.can_create %}
<a href="{% url 'add_book' %}">Add New Book</a>
{% endif %} {% if perms.relationship_app.can_delete %}
<a href="{% url 'delete_book' book.pk %}">Delete</a>
{% endif %}
```

## Admin Interface

Groups and permissions can be managed through Django's admin interface:

- Navigate to `/admin/auth/group/` to manage groups
- Navigate to `/admin/auth/permission/` to view all permissions
- Navigate to `/admin/auth/user/` to assign users to groups

## Security Notes

- All views use `raise_exception=True` to return HTTP 403 Forbidden instead of redirecting to login
- Permissions are checked at the view level using decorators
- Users must be authenticated to access any protected views
- The system uses Django's built-in permission framework for security

## File Structure

```
relationship_app/
├── models.py              # Custom permissions defined
├── views.py               # Permission-protected views
├── forms.py               # Forms for Book and Author
├── urls.py                # URL patterns
├── management/
│   └── commands/
│       ├── setup_groups.py        # Create groups and permissions
│       └── create_test_users.py   # Create test users
└── templates/
    └── relationship_app/
        ├── list_authors.html
        ├── add_author.html
        └── change_author.html
```

This implementation provides a robust, scalable permission system that can be easily extended for additional models and permission types.
