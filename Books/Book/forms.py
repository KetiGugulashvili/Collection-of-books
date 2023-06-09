from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title',
                  'author',
                  'publication_date',
                  'isbn_number',
                  'number_of_pages',
                  'cover_link',
                  'publication_language']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'})
        }
