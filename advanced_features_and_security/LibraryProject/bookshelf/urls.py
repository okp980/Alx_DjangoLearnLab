from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    # Book management views with permission requirements
    path('', views.book_list, name='book_list'),
    path('books/', views.book_list, name='book_list'),
    path('book-list/', views.book_list, name='list_books'),  # Alias for backward compatibility
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    
    # User dashboard
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
]
