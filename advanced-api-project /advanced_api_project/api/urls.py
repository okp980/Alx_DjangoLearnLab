from django.urls import path
from api.views import CreateBookView, ListBookView, RetrieveBookView, UpdateBookView, DeleteBookView

urlpatterns = [
    path('books/', CreateBookView.as_view(), name='create-book'),
    path('books/', ListBookView.as_view(), name='list-book'),
    path('books/<int:pk>/', RetrieveBookView.as_view(), name='retrieve-book'),
    path('books/<int:pk>/', UpdateBookView.as_view(), name='update-book'),
    path('books/<int:pk>/', DeleteBookView.as_view(), name='delete-book'),
]