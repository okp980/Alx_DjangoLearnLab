from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.html import escape
import logging
from .models import Book, CustomUser
from .forms import BookForm

# Create your views here.

# SECURITY: Configure logging for security events
security_logger = logging.getLogger('django.security')


@permission_required('bookshelf.can_view', raise_exception=True)
@csrf_protect
def book_list(request):
    """
    SECURITY: View to list all books with enhanced security measures.
    
    Security features implemented:
    - CSRF protection via @csrf_protect decorator
    - Permission-based access control
    - Input validation for search parameters
    - SQL injection prevention via Django ORM
    """
    try:
        # SECURITY: Use Django ORM to prevent SQL injection
        # Never use raw SQL or string formatting with user input
        books = Book.objects.select_related('borrower').all()
        
        # SECURITY: Handle search functionality safely
        search_query = request.GET.get('search', '').strip()
        if search_query:
            # SECURITY: Escape user input and use parameterized queries
            search_query = escape(search_query)
            books = books.filter(
                title__icontains=search_query
            ).union(
                books.filter(author__icontains=search_query)
            )
        
        context = {
            'books': books,
            'search_query': search_query,
        }
        
        return render(request, 'bookshelf/list_books.html', context)
        
    except Exception as e:
        # SECURITY: Log security-related errors
        security_logger.error(f"Error in book_list view: {str(e)}")
        messages.error(request, 'An error occurred while retrieving books.')
        return render(request, 'bookshelf/list_books.html', {'books': []})

@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    """View to list all books - requires can_view permission (alias for book_list)"""
    return book_list(request)

@permission_required('bookshelf.can_create', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def add_book(request):
    """
    SECURITY: View to add a new book with enhanced security measures.
    
    Security features implemented:
    - CSRF protection
    - HTTP method restriction (GET/POST only)
    - Input validation via Django forms
    - Database integrity error handling
    - Security logging
    """
    if request.method == 'POST':
        try:
            form = BookForm(request.POST)
            if form.is_valid():
                # SECURITY: Use form.save() which automatically escapes data
                book = form.save()
                
                # SECURITY: Log successful book creation
                security_logger.info(
                    f"Book '{book.title}' created by user: {request.user.username}"
                )
                
                messages.success(request, 'Book added successfully!')
                return HttpResponseRedirect(reverse('bookshelf:book_list'))
            else:
                # SECURITY: Log form validation errors
                security_logger.warning(
                    f"Form validation failed for book creation by user: {request.user.username}. "
                    f"Errors: {form.errors}"
                )
        except IntegrityError as e:
            # SECURITY: Handle database integrity errors
            security_logger.error(f"Database integrity error in add_book: {str(e)}")
            messages.error(request, 'A book with this information already exists.')
            form = BookForm(request.POST)
        except Exception as e:
            # SECURITY: Log unexpected errors
            security_logger.error(f"Unexpected error in add_book: {str(e)}")
            messages.error(request, 'An error occurred while adding the book.')
            form = BookForm()
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/add_book.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def edit_book(request, pk):
    """
    SECURITY: View to edit an existing book with enhanced security measures.
    
    Security features implemented:
    - CSRF protection
    - HTTP method restriction
    - Input validation via Django forms
    - Primary key validation
    - Security logging
    """
    try:
        # SECURITY: Validate primary key to prevent injection
        if not pk or not str(pk).isdigit():
            security_logger.warning(f"Invalid primary key in edit_book: {pk}")
            messages.error(request, 'Invalid book ID.')
            return HttpResponseRedirect(reverse('bookshelf:book_list'))
        
        # SECURITY: Use get_object_or_404 to safely retrieve the book
        book = get_object_or_404(Book, pk=pk)
        
        if request.method == 'POST':
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                # SECURITY: Log book modification
                security_logger.info(
                    f"Book '{book.title}' modified by user: {request.user.username}"
                )
                form.save()
                messages.success(request, 'Book updated successfully!')
                return HttpResponseRedirect(reverse('bookshelf:book_list'))
            else:
                # SECURITY: Log form validation errors
                security_logger.warning(
                    f"Form validation failed for book edit by user: {request.user.username}. "
                    f"Errors: {form.errors}"
                )
        else:
            form = BookForm(instance=book)
            
    except Exception as e:
        # SECURITY: Log unexpected errors
        security_logger.error(f"Unexpected error in edit_book: {str(e)}")
        messages.error(request, 'An error occurred while editing the book.')
        return HttpResponseRedirect(reverse('bookshelf:book_list'))
    
    return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})

@permission_required('bookshelf.can_delete', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def delete_book(request, pk):
    """
    SECURITY: View to delete a book with enhanced security measures.
    
    Security features implemented:
    - CSRF protection
    - HTTP method restriction
    - Primary key validation
    - Confirmation required (POST only)
    - Security logging
    """
    try:
        # SECURITY: Validate primary key to prevent injection
        if not pk or not str(pk).isdigit():
            security_logger.warning(f"Invalid primary key in delete_book: {pk}")
            messages.error(request, 'Invalid book ID.')
            return HttpResponseRedirect(reverse('bookshelf:book_list'))
        
        # SECURITY: Use get_object_or_404 to safely retrieve the book
        book = get_object_or_404(Book, pk=pk)
        
        if request.method == 'POST':
            # SECURITY: Log book deletion attempt
            book_title = book.title
            security_logger.info(
                f"Book '{book_title}' deleted by user: {request.user.username}"
            )
            
            book.delete()
            messages.success(request, f'Book "{book_title}" deleted successfully!')
            return HttpResponseRedirect(reverse('bookshelf:book_list'))
        
    except Exception as e:
        # SECURITY: Log unexpected errors
        security_logger.error(f"Unexpected error in delete_book: {str(e)}")
        messages.error(request, 'An error occurred while deleting the book.')
        return HttpResponseRedirect(reverse('bookshelf:book_list'))
    
    return render(request, 'bookshelf/delete_book.html', {'book': book})

@login_required
@csrf_protect
def book_detail(request, pk):
    """
    SECURITY: View to show book details with enhanced security measures.
    
    Security features implemented:
    - Login required
    - CSRF protection
    - Primary key validation
    - Security logging
    """
    try:
        # SECURITY: Validate primary key to prevent injection
        if not pk or not str(pk).isdigit():
            security_logger.warning(f"Invalid primary key in book_detail: {pk}")
            messages.error(request, 'Invalid book ID.')
            return HttpResponseRedirect(reverse('bookshelf:book_list'))
        
        # SECURITY: Use get_object_or_404 to safely retrieve the book
        book = get_object_or_404(Book, pk=pk)
        
        # SECURITY: Log book access
        security_logger.info(
            f"Book '{book.title}' accessed by user: {request.user.username}"
        )
        
        return render(request, 'bookshelf/book_detail.html', {'book': book})
        
    except Exception as e:
        # SECURITY: Log unexpected errors
        security_logger.error(f"Unexpected error in book_detail: {str(e)}")
        messages.error(request, 'An error occurred while retrieving book details.')
        return HttpResponseRedirect(reverse('bookshelf:book_list'))


@login_required
@csrf_protect
def user_dashboard(request):
    """
    SECURITY: Dashboard showing user's permissions and available actions.
    
    Security features implemented:
    - Login required
    - CSRF protection
    - Permission checking
    - Security logging
    """
    try:
        user = request.user
        user_groups = user.groups.all()
        
        # SECURITY: Check user permissions securely
        permissions = {
            'can_view': user.has_perm('bookshelf.can_view'),
            'can_create': user.has_perm('bookshelf.can_create'),
            'can_edit': user.has_perm('bookshelf.can_edit'),
            'can_delete': user.has_perm('bookshelf.can_delete'),
        }
        
        # SECURITY: Log dashboard access
        security_logger.info(
            f"User dashboard accessed by: {request.user.username}"
        )
        
        context = {
            'user': user,
            'user_groups': user_groups,
            'permissions': permissions,
        }
        return render(request, 'bookshelf/user_dashboard.html', context)
        
    except Exception as e:
        # SECURITY: Log unexpected errors
        security_logger.error(f"Unexpected error in user_dashboard: {str(e)}")
        messages.error(request, 'An error occurred while loading the dashboard.')
        return HttpResponseRedirect(reverse('bookshelf:book_list'))
