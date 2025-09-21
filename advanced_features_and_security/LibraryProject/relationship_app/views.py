from django.shortcuts import render, get_object_or_404
from .models import Library, Book, Author, UserProfile
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from .forms import BookForm, AuthorForm
from django.contrib.auth.decorators import permission_required

# Create your views here.

@permission_required('relationship_app.can_view', raise_exception=True)
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

@permission_required('relationship_app.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('list_books'))
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_edit', raise_exception=True)
def change_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('list_books'))
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/change_book.html', {'form': form})

@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    return HttpResponseRedirect(reverse('list_books'))

# Author management views
@permission_required('relationship_app.can_view', raise_exception=True)
def list_authors(request):
    authors = Author.objects.all()
    return render(request, 'relationship_app/list_authors.html', {'authors': authors})

@permission_required('relationship_app.can_create', raise_exception=True)
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('list_authors'))
    else:
        form = AuthorForm()
    return render(request, 'relationship_app/add_author.html', {'form': form})

@permission_required('relationship_app.can_edit', raise_exception=True)
def change_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('list_authors'))
    else:
        form = AuthorForm(instance=author)
    return render(request, 'relationship_app/change_author.html', {'form': form})

@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    author.delete()
    return HttpResponseRedirect(reverse('list_authors'))

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Role-based access control functions
def is_admin(user):
    """Check if user has admin role"""
    if not user.is_authenticated:
        return False
    try:
        user_profile = UserProfile.objects.get(user=user)
        return user_profile.role == 'admin'
    except UserProfile.DoesNotExist:
        return False

def is_librarian(user):
    """Check if user has librarian role"""
    if not user.is_authenticated:
        return False
    try:
        user_profile = UserProfile.objects.get(user=user)
        return user_profile.role == 'librarian'
    except UserProfile.DoesNotExist:
        return False

def is_member(user):
    """Check if user has member role"""
    if not user.is_authenticated:
        return False
    try:
        user_profile = UserProfile.objects.get(user=user)
        return user_profile.role == 'member'
    except UserProfile.DoesNotExist:
        return False

# Role-based class views
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminView(TemplateView):
    """Admin-only class view for managing the entire system"""
    template_name = 'relationship_app/admin_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user_role': 'Admin',
            'message': 'Welcome to the Admin Dashboard! You have full system access.',
            'available_actions': [
                'Manage all users',
                'Configure system settings',
                'View system logs',
                'Manage libraries and books',
                'Assign user roles'
            ]
        })
        return context

@method_decorator(user_passes_test(is_librarian), name='dispatch')
class LibrarianView(TemplateView):
    """Librarian-only class view for managing library operations"""
    template_name = 'relationship_app/librarian_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user_role': 'Librarian',
            'message': 'Welcome to the Librarian Dashboard! You can manage library operations.',
            'available_actions': [
                'Manage books and authors',
                'Handle book loans',
                'View member information',
                'Generate library reports',
                'Manage library inventory'
            ]
        })
        return context

@method_decorator(user_passes_test(is_member), name='dispatch')
class MemberView(TemplateView):
    """Member-only class view for library users"""
    template_name = 'relationship_app/member_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user_role': 'Member',
            'message': 'Welcome to the Member Dashboard! You can browse and borrow books.',
            'available_actions': [
                'Browse available books',
                'View borrowing history',
                'Request book loans',
                'Update personal information',
                'View library announcements'
            ]
        })
        return context