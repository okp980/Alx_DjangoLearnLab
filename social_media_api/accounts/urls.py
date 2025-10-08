from rest_framework.authtoken import views
from django.urls import path
from accounts.views import RegisterView, ProfileView

urlpatterns = [
    path("login", views.obtain_auth_token, name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("profile", ProfileView.as_view(), name="profile"),
]
