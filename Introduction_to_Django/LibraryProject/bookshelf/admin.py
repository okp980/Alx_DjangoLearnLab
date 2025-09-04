from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters in the right sidebar
    list_filter = ('author', 'publication_year')
    
    # Add search functionality
    search_fields = ('title', 'author')
    
    # Number of items per page
    list_per_page = 25
    
    # Enable ordering by clicking column headers
    ordering = ('title',)
    
    # Add date hierarchy if you have date fields (optional)
    # date_hierarchy = 'publication_year'
    
    # Customize the admin form
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year')
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

# Register the model with the custom admin class
admin.site.register(Book, BookAdmin)
