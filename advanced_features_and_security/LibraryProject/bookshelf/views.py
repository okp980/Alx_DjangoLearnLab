from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Book, CustomUser
from .forms import BookForm

# Create your views here.

@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    """View to list all books - requires can_view permission"""
    books = Book.objects.all()
    return render(request, 'bookshelf/list_books.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    """View to add a new book - requires can_create permission"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return HttpResponseRedirect(reverse('list_books'))
    else:
        form = BookForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    """View to edit an existing book - requires can_edit permission"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return HttpResponseRedirect(reverse('list_books'))
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    """View to delete a book - requires can_delete permission"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return HttpResponseRedirect(reverse('list_books'))
    return render(request, 'bookshelf/delete_book.html', {'book': book})

@login_required
def book_detail(request, pk):
    """View to show book details - requires login"""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@login_required
def user_dashboard(request):
    """Dashboard showing user's permissions and available actions"""
    user = request.user
    user_groups = user.groups.all()
    
    # Check user permissions
    permissions = {
        'can_view': user.has_perm('bookshelf.can_view'),
        'can_create': user.has_perm('bookshelf.can_create'),
        'can_edit': user.has_perm('bookshelf.can_edit'),
        'can_delete': user.has_perm('bookshelf.can_delete'),
    }
    
    context = {
        'user': user,
        'user_groups': user_groups,
        'permissions': permissions,
    }
    return render(request, 'bookshelf/user_dashboard.html', context)
