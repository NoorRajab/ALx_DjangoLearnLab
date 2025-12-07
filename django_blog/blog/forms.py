# blog/forms.py (Updated)
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment

# Existing Form (from Task 1)
class CustomUserCreationForm(UserCreationForm):
    
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name') 
        
# ----------------
# New: Post ModelForm
# ----------------
class PostForm(forms.ModelForm):
    """Form used for creating and updating blog posts."""
    class Meta:
        model = Post
        # We only include title and content, as author is set automatically
        # and published_date is set by auto_now_add.
        fields = ['title', 'content'] 
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15, 'cols': 80}),
        }
class CommentForm(forms.ModelForm):
    """Form used for creating and updating comments."""
    class Meta:
        model = Comment
        # Only the content field is needed, as post and author are set by the view.
        fields = ['content'] 
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
        }