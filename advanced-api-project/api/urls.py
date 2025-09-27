from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import  AuthorViewSet
from api.views import ListView, DetailView, CreateView, UpdateView, DeleteView
router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
urlpatterns = [
    path('', include(router.urls)),
    path('books/', ListView.as_view(), name='book-list'),
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),
    path('books/create', CreateView.as_view(), name='book-create'),
    path('books/update/<int:pk>/', UpdateView.as_view(), name='book-update'),
    path('books/delete/<int:pk>/', DeleteView.as_view(), name='book-delete'),
]