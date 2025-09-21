from django.urls import path
from .views import list_books, AdminView, LibrarianView, MemberView
from .views import LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Role-based class views
    path('admin/', AdminView.as_view(), name='admin_view'),
    path('librarian/', LibrarianView.as_view(), name='librarian_view'),
    path('member/', MemberView.as_view(), name='member_view'),
    
    # Book-related views
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.change_book, name='change_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
]