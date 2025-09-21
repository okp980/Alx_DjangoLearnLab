from django import forms
from .models import Book, CustomUser


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
