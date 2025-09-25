from django.urls import include, path
from .views import BookViewSet
from rest_framework.routers import DefaultRouter
from .views import BookList
from rest_framework.authtoken import views

router = DefaultRouter()

router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('books/', BookList.as_view(),name='book-list'),
    path('', include(router.urls)),
]


   