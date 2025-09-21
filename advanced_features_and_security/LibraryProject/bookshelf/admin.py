from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import CustomUser, Book

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

class BookAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('title', 'author', 'publication_year', 'borrower')
    
    # Add filters in the right sidebar
    list_filter = ('author', 'publication_year', 'borrower')
    
    # Add search functionality
    search_fields = ('title', 'author', 'borrower__email', 'borrower__username')
    
    # Number of items per page
    list_per_page = 25
    
    # Enable ordering by clicking column headers
    ordering = ('title',)
    
    # Add date hierarchy if you have date fields (optional)
    # date_hierarchy = 'publication_year'
    
    # Customize the admin form
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year', 'borrower')
        }),
    )
    
    # Add actions (optional)
    actions = ['mark_as_recent']
    
    def mark_as_recent(self, request, queryset):
        """Custom action to mark books as recent (published in last 5 years)"""
        current_year = 2024  # You might want to make this dynamic
        recent_count = queryset.filter(publication_year__gte=current_year-5).count()
        self.message_user(request, f'{recent_count} books are already recent (published in last 5 years).')
    mark_as_recent.short_description = "Check for recent publications"

# Register the models with the custom admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)
