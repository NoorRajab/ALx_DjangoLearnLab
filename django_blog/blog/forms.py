
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    # Add email field, making it required
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        # Include all fields from the base form, plus the new 'email' field
        fields = ('username', 'email', 'first_name', 'last_name')