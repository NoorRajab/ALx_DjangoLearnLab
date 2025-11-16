

from django import forms
from .models import Book # Still needed for BookForm, if we keep it
# If you are removing BookForm, adjust the import of Book, or remove it if not needed

# Assuming we keep BookForm and add ExampleForm
class BookForm(forms.ModelForm):
    # (Existing BookForm definition remains here)
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year'] 
        
        # Optional: Add help text or widgets for better UX
        widgets = {
            'publication_year': forms.NumberInput(attrs={'min': 1000, 'max': 2100}),
        }

# --- The requested ExampleForm ---
class ExampleForm(forms.Form):
    """
    A simple demonstration form that does not bind directly to a model.
    """
    # Define fields relevant to the example usage
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