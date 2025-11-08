# relationship_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

# Import your existing models/views
from .models import Book, Library
from django.views.generic import DetailView # Already defined in previous task

# --- 1. Registration View (Function-Based) ---
def register_view(request):
    """Handles user registration using Django's UserCreationForm."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after successful registration
            login(request, user)
            # Redirect to a desired page (e.g., the book list)
            return redirect('relationship_app:book-list')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    # Renders the 'relationship_app/register.html' template
    return render(request, 'relationship_app/register.html', context)


# --- 2. Login View (Class-Based - using Django's built-in) ---
class CustomLoginView(LoginView):
    """Custom LoginView to specify the template and context."""
    # Specifies the template to use
    template_name = 'relationship_app/login.html'
    
    # Optional: Specifies the fields to display for the form (default is username and password)
    # fields = '__all__' 
    
    # Specifies where to go after a successful login (lazy loading)
    next_page = reverse_lazy('relationship_app:book-list')


# --- 3. Logout View (Class-Based - using Django's built-in) ---
class CustomLogoutView(LogoutView):
    """Custom LogoutView to specify the template."""
    # Specifies the template to display after logout
    next_page = reverse_lazy('relationship_app:logout') # Redirect to the logout success page itself
    template_name = 'relationship_app/logout.html'

# (Keep your existing book_list_view and LibraryDetailView here)
# ...