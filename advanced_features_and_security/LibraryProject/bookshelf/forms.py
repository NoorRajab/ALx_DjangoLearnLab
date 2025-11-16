

from django import forms
from .models import Book 
class BookForm(forms.ModelForm):
   
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year'] 
        
       
        widgets = {
            'publication_year': forms.NumberInput(attrs={'min': 1000, 'max': 2100}),
        }

class ExampleForm(forms.Form):
   
    user_feedback = forms.CharField(
        label='Your Feedback',
        max_length=500,
        widget=forms.Textarea
    )
    rating = forms.IntegerField(
        label='Rating (1-5)',
        min_value=1,
        max_value=5
    )