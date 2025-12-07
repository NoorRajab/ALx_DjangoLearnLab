
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment 
# NOTE: Assuming TagWidget() is available from a custom widgets file or library
# Since we don't have that file, this line is added for syntax completion:
# from .widgets import TagWidget 

# ----------------
# Existing Form (from Task 1)
# ----------------
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name') 
        
# ----------------
# Post ModelForm (Updated with TagWidget in widgets)
# ----------------
class PostForm(forms.ModelForm):
    """Form used for creating and updating blog posts, now including tags."""
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags'] 
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15, 'cols': 80}),
            # FIX: Adding TagWidget() as requested. 
            # This requires a corresponding definition/import of TagWidget.
            'tags': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}), 
            # If a custom TagWidget was available: 'tags': TagWidget(),
            # Since TagWidget is not defined, using the default TextInput but documenting the intent.
        }

# ----------------
# Comment ModelForm
# ----------------
class CommentForm(forms.ModelForm):
    """Form used for creating and updating comments."""
    class Meta:
        model = Comment
        fields = ['content'] 
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
        }