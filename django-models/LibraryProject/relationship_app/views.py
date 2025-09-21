from django.shortcuts import render
from .models import Library, Book, UserProfile
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse

# Create your views here.

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

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

# Role-based views
@user_passes_test(is_admin)
def admin_view(request):
    """Admin-only view for managing the entire system"""
    context = {
        'user_role': 'Admin',
        'message': 'Welcome to the Admin Dashboard! You have full system access.',
        'available_actions': [
            'Manage all users',
            'Configure system settings',
            'View system logs',
            'Manage libraries and books',
            'Assign user roles'
        ]
    }
    return render(request, 'relationship_app/admin_view.html', context)

@user_passes_test(is_librarian)
def librarian_view(request):
    """Librarian-only view for managing library operations"""
    context = {
        'user_role': 'Librarian',
        'message': 'Welcome to the Librarian Dashboard! You can manage library operations.',
        'available_actions': [
            'Manage books and authors',
            'Handle book loans',
            'View member information',
            'Generate library reports',
            'Manage library inventory'
        ]
    }
    return render(request, 'relationship_app/librarian_view.html', context)

@user_passes_test(is_member)
def member_view(request):
    """Member-only view for library users"""
    context = {
        'user_role': 'Member',
        'message': 'Welcome to the Member Dashboard! You can browse and borrow books.',
        'available_actions': [
            'Browse available books',
            'View borrowing history',
            'Request book loans',
            'Update personal information',
            'View library announcements'
        ]
    }
    return render(request, 'relationship_app/member_view.html', context)