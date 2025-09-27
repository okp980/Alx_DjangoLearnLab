from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from api.models import Book, Author
from api.serializers import BookSerializer, AuthorSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

    
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'publication_year', 'author__name']
    ordering_fields = ['publication_year', 'title']
    ordering = ['publication_year', 'title']
    

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']