from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import UserManager
# from . import signals
# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user manager for the CustomUser model.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser with additional fields.
    """
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    objects: 'CustomUserManager' = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    
class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    class Meta:
        permissions = (
            ('can_add_book', 'Can add book'),
            ('can_change_book', 'Can change book'),
            ('can_delete_book', 'Can delete book'),
        )
    
    
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)
    
    def __str__(self):
        return self.name
    
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ROLE_STATUS = (
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    )
    role = models.CharField(max_length=100, choices=ROLE_STATUS, default='member')
    
    def __str__(self):
        return self.user.username

    