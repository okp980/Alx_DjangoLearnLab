from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    # Book management views with permission requirements
    path('', views.list_books, name='list_books'),
    path('books/', views.list_books, name='list_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    
    # User dashboard
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
]
