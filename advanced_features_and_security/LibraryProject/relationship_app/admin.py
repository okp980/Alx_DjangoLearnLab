from django.contrib import admin
from .models import Book, Library, Librarian, UserProfile

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')