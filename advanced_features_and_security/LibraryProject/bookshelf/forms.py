from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.html import escape
from .models import Book, CustomUser


class ExampleForm(forms.Form):
    """
    Example form demonstrating various form fields and security practices.
    
    This form showcases:
    - Different field types
    - Input validation
    - Security measures
    - Custom widgets
    - Error handling
    """
    
    # Text fields with different validation
    title = forms.CharField(
        max_length=200,
        min_length=2,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter book title',
            'maxlength': '200'
        }),
        label='Book Title',
        help_text='Enter a descriptive title (2-200 characters)'
    )
    
    author = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter author name',
            'maxlength': '100'
        }),
        label='Author Name'
    )
    
    # Email field with validation
    contact_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'author@example.com'
        }),
        label='Contact Email',
        help_text='Optional: Author contact email'
    )
    
    # Number field with range validation
    publication_year = forms.IntegerField(
        min_value=1000,
        max_value=2024,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '2023',
            'min': '1000',
            'max': '2024'
        }),
        label='Publication Year',
        help_text='Year between 1000 and 2024'
    )
    
    # Choice field
    GENRE_CHOICES = [
        ('', 'Select a genre'),
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('mystery', 'Mystery'),
        ('romance', 'Romance'),
        ('sci-fi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('other', 'Other'),
    ]
    
    genre = forms.ChoiceField(
        choices=GENRE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Genre',
        required=False
    )
    
    # Textarea field
    description = forms.CharField(
        required=False,
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter book description...',
            'maxlength': '1000'
        }),
        label='Description',
        help_text='Optional: Brief description of the book (max 1000 characters)'
    )
    
    # Boolean field
    is_featured = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Featured Book',
        help_text='Check if this should be featured on the homepage'
    )
    
    # Date field
    availability_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Available From',
        help_text='When will this book be available for borrowing?'
    )
    
    # File upload field (with security restrictions)
    cover_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        label='Cover Image',
        help_text='Upload a book cover image (JPG, PNG, GIF - max 5MB)'
    )
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with additional security measures."""
        super().__init__(*args, **kwargs)
        
        # SECURITY: Add CSRF token field (though Django handles this automatically)
        # SECURITY: Set additional security attributes on fields
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'attrs'):
                # Add security attributes to input fields
                if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.NumberInput)):
                    field.widget.attrs.update({
                        'autocomplete': 'off',  # Prevent autocomplete for sensitive fields
                    })
    
    def clean_title(self):
        """
        SECURITY: Custom validation for title field.
        
        This method demonstrates:
        - Input sanitization
        - Validation logic
        - Error handling
        """
        title = self.cleaned_data.get('title', '').strip()
        
        # SECURITY: Escape HTML content to prevent XSS
        title = escape(title)
        
        # Validation: Check for minimum length after stripping
        if len(title) < 2:
            raise ValidationError('Title must be at least 2 characters long.')
        
        # Validation: Check for prohibited words (example)
        prohibited_words = ['spam', 'test', 'dummy']
        if any(word.lower() in title.lower() for word in prohibited_words):
            raise ValidationError('Title contains prohibited words.')
        
        return title
    
    def clean_author(self):
        """SECURITY: Custom validation for author field."""
        author = self.cleaned_data.get('author', '').strip()
        
        # SECURITY: Escape HTML content
        author = escape(author)
        
        # Validation: Check for valid author name format
        if not author.replace(' ', '').replace('-', '').replace("'", '').isalpha():
            raise ValidationError('Author name should contain only letters, spaces, hyphens, and apostrophes.')
        
        return author
    
    def clean_contact_email(self):
        """Custom validation for contact email."""
        email = self.cleaned_data.get('contact_email', '').strip()
        
        if email:
            # SECURITY: Validate email format (Django's EmailField already does this)
            # Additional validation: Check for disposable email domains
            disposable_domains = ['tempmail.com', '10minutemail.com', 'guerrillamail.com']
            domain = email.split('@')[1].lower() if '@' in email else ''
            
            if domain in disposable_domains:
                raise ValidationError('Please use a permanent email address.')
        
        return email
    
    def clean_cover_image(self):
        """
        SECURITY: Custom validation for file uploads.
        
        This demonstrates file upload security:
        - File size validation
        - File type validation
        - Security checks
        """
        image = self.cleaned_data.get('cover_image')
        
        if image:
            # SECURITY: Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:  # 5MB in bytes
                raise ValidationError('Image file size cannot exceed 5MB.')
            
            # SECURITY: Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if image.content_type not in allowed_types:
                raise ValidationError('Only JPG, PNG, and GIF images are allowed.')
            
            # SECURITY: Check file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            file_extension = image.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise ValidationError('Invalid file extension. Only JPG, PNG, and GIF are allowed.')
        
        return image
    
    def clean(self):
        """
        SECURITY: Form-wide validation.
        
        This method runs after individual field validation and allows
        for cross-field validation and additional security checks.
        """
        cleaned_data = super().clean()
        
        # Cross-field validation example
        publication_year = cleaned_data.get('publication_year')
        availability_date = cleaned_data.get('availability_date')
        
        if publication_year and availability_date:
            if availability_date.year < publication_year:
                raise ValidationError('Availability date cannot be before publication year.')
        
        # SECURITY: Log form submission attempts
        # In a real application, you might want to log this for security monitoring
        import logging
        logger = logging.getLogger('django.security')
        logger.info(f"ExampleForm submitted with title: {cleaned_data.get('title', 'N/A')}")
        
        return cleaned_data


class BookForm(forms.ModelForm):
    """Form for creating and editing Book instances"""
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'borrower']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter publication year'}),
            'borrower': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Book Title',
            'author': 'Author',
            'publication_year': 'Publication Year',
            'borrower': 'Borrower (Optional)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show users who are not already borrowing a book
        self.fields['borrower'].queryset = CustomUser.objects.filter(book__isnull=True)
        self.fields['borrower'].empty_label = "No borrower"
    
    def clean_publication_year(self):
        """Validate publication year"""
        year = self.cleaned_data.get('publication_year')
        if year and (year < 1000 or year > 2024):
            raise forms.ValidationError("Please enter a valid publication year.")
        return year
