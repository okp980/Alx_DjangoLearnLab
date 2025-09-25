from django.urls import include, path
from .views import BookViewSet
from rest_framework.routers import DefaultRouter
from .views import BookList

router = DefaultRouter()

router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(),name='book-list'),
    path('', include(router.urls)),
]


   