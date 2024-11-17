from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'publication_date']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }
