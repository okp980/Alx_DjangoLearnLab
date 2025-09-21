# Bookshelf App - Custom Permissions and Groups Implementation

This document explains the custom permissions and user groups implementation in the Bookshelf app of the Library Project.

## Overview

The Bookshelf app implements a comprehensive permission system with custom permissions and user groups to control access to different actions on the Book model. This system provides fine-grained access control for library management operations.

## Custom Permissions

### Book Model (`bookshelf/models.py`)

The Book model includes custom permissions defined in the Meta class:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    borrower = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
        )
```

## User Groups

The system defines three main user groups with different permission levels:

### 1. Viewers Group

- **Permissions**: `can_view` for Book model
- **Description**: Users who can only view books
- **Use Case**: Regular library members who can browse the catalog

### 2. Editors Group

- **Permissions**: `can_view`, `can_create`, `can_edit` for Book model
- **Description**: Users who can view, create, and edit books
- **Use Case**: Librarians who manage the library catalog

### 3. Admins Group

- **Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete` for Book model
- **Description**: Users who have full access including delete permissions
- **Use Case**: System administrators with complete control

## Permission Enforcement in Views

All views are protected using Django's `@permission_required` decorator with `raise_exception=True`:

### Book Management Views (`bookshelf/views.py`)

```python
@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    """View to list all books - requires can_view permission"""

@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    """View to add a new book - requires can_create permission"""

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    """View to edit an existing book - requires can_edit permission"""

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    """View to delete a book - requires can_delete permission"""

@login_required
def book_detail(request, pk):
    """View to show book details - requires login"""

@login_required
def user_dashboard(request):
    """Dashboard showing user's permissions and available actions"""
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
   - Should be able to view books and book details
   - Should get 403 Forbidden when trying to create/edit/delete
   - Dashboard should show only "View Books" permission

3. **Test Editor User**:

   - Login as `editor_user`
   - Should be able to view, create, and edit books
   - Should get 403 Forbidden when trying to delete
   - Dashboard should show "View", "Create", and "Edit" permissions

4. **Test Admin User**:
   - Login as `admin_user`
   - Should have full access to all operations
   - Dashboard should show all permissions including "Delete"

### URL Endpoints for Testing

- Book List: `/bookshelf/` or `/`
- Add Book: `/bookshelf/books/add/`
- Book Detail: `/bookshelf/books/<id>/`
- Edit Book: `/bookshelf/books/<id>/edit/`
- Delete Book: `/bookshelf/books/<id>/delete/`
- User Dashboard: `/bookshelf/dashboard/`

## Permission Checking in Templates

The templates include permission checks using the `perms` template variable:

```html
{% if perms.bookshelf.can_create %}
<a href="{% url 'bookshelf:add_book' %}" class="btn btn-success"
  >Add New Book</a
>
{% endif %} {% if perms.bookshelf.can_edit %}
<a href="{% url 'bookshelf:edit_book' book.pk %}" class="btn btn-warning"
  >Edit</a
>
{% endif %} {% if perms.bookshelf.can_delete %}
<a href="{% url 'bookshelf:delete_book' book.pk %}" class="btn btn-danger"
  >Delete</a
>
{% endif %}
```

## Forms and Validation

### BookForm (`bookshelf/forms.py`)

The BookForm includes:

- Custom widgets for better styling
- Validation for publication year
- Dynamic borrower queryset (only users not already borrowing books)
- Proper labels and placeholders

## Templates

The app includes comprehensive HTML templates:

- `list_books.html` - Shows all books with permission-based actions
- `add_book.html` - Form for creating new books
- `edit_book.html` - Form for editing existing books
- `delete_book.html` - Confirmation page for deleting books
- `book_detail.html` - Detailed view of a single book
- `user_dashboard.html` - User's permission overview and available actions

## Admin Interface

Groups and permissions can be managed through Django's admin interface:

- Navigate to `/admin/auth/group/` to manage groups
- Navigate to `/admin/auth/permission/` to view all permissions
- Navigate to `/admin/auth/user/` to assign users to groups

## Security Features

- All views use `raise_exception=True` to return HTTP 403 Forbidden instead of redirecting to login
- Permissions are checked at the view level using decorators
- Users must be authenticated to access any protected views
- The system uses Django's built-in permission framework for security
- Custom user model (`CustomUser`) extends Django's AbstractUser

## File Structure

```
bookshelf/
├── models.py              # Custom permissions defined in Book model
├── views.py               # Permission-protected views
├── forms.py               # BookForm with validation
├── urls.py                # URL patterns with app_name
├── management/
│   └── commands/
│       ├── setup_groups.py        # Create groups and permissions
│       └── create_test_users.py   # Create test users
└── templates/
    └── bookshelf/
        ├── list_books.html
        ├── add_book.html
        ├── edit_book.html
        ├── delete_book.html
        ├── book_detail.html
        └── user_dashboard.html
```

## Key Features

1. **Custom User Model**: Uses `CustomUser` extending `AbstractUser`
2. **Permission-Based Access Control**: Four distinct permission levels
3. **User Groups**: Three predefined groups with appropriate permissions
4. **Comprehensive Views**: Full CRUD operations with permission checks
5. **User Dashboard**: Shows user's permissions and available actions
6. **Responsive Templates**: Clean, styled HTML templates
7. **Form Validation**: Proper validation and error handling
8. **Management Commands**: Easy setup and testing tools

## Usage Examples

### Checking Permissions in Code

```python
# In views
if request.user.has_perm('bookshelf.can_create'):
    # Allow creation

# In templates
{% if perms.bookshelf.can_delete %}
    <!-- Show delete button -->
{% endif %}
```

### Assigning Users to Groups

```python
from django.contrib.auth.models import Group
from bookshelf.models import CustomUser

user = CustomUser.objects.get(username='some_user')
group = Group.objects.get(name='Editors')
user.groups.add(group)
```

This implementation provides a robust, scalable permission system specifically designed for the Bookshelf app, with comprehensive testing tools and documentation.
