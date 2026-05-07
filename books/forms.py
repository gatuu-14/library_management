from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publisher', 'publication_year', 
                 'category', 'total_copies', 'available_copies', 'location', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book Title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author Name'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN Number'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Publisher'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year'}),
            'category': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('Fiction', 'Fiction'), ('Non-Fiction', 'Non-Fiction'), 
                ('Science', 'Science'), ('Technology', 'Technology'),
                ('History', 'History'), ('Biography', 'Biography'),
                ('Children', 'Children'), ('Other', 'Other')
            ]),
            'total_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shelf Location'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SearchForm(forms.Form):
    search_type = forms.ChoiceField(choices=[
        ('title', 'Title'),
        ('author', 'Author'),
        ('isbn', 'ISBN'),
        ('category', 'Category'),
    ], widget=forms.Select(attrs={'class': 'form-control'}))
    
    query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Enter search term...'
    }))

class BorrowForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'User ID'
    }))