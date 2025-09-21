from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import CustomUser, Book, Library, Librarian, UserProfile

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin interface for the CustomUser model.
    """
    # Fields to display in the user list
    list_display = ('email', 'username', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active', 'profile_photo_preview')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'date_of_birth')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    # Fields for the user detail form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields for creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth'),
        }),
    )
    
    # Read-only fields
    readonly_fields = ('date_joined', 'last_login')
    
    def profile_photo_preview(self, obj):
        """
        Display a thumbnail preview of the profile photo in the admin list.
        """
        if obj.profile_photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_photo.url)
        return "No photo"
    profile_photo_preview.short_description = "Profile Photo"

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