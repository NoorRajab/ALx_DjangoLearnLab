# relationship_app/views.py
from django.shortcuts import render
from django.views.generic.detail import DetailView # Previous correction retained
from .models import Library, Book
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

# --- 1. Implement Function-based View ---

def list_books(request): # CORRECTED: Changed name from book_list_view to list_books
    """
    Function-based view to list all books.
    Queries all books and renders the list_books.html template.
    """
    # Query all books, using select_related('author') for optimization
    all_books = Book.objects.all().select_related('author')
    
    context = {
        'books': all_books,
    }
    
    # Render the template
    return render(request, 'relationship_app/list_books.html', context)

# --- 2. Implement Class-based View (DetailView) ---

class LibraryDetailView(DetailView):
    """
    Class-based view (DetailView) to show details for a specific library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library' 
    
    def get_queryset(self):
        return Library.objects.all().prefetch_related('books__author')

# (Authentication and RBAC views would follow here, with their names remaining unchanged)
# ...
def register_view(request):
    """Handles user registration using Django's UserCreationForm."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after successful registration
            login(request, user)
            # Redirect to the main book list page (using the corrected name 'book-list')
            return redirect('relationship_app:book-list')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    # Renders the 'relationship_app/register.html' template
    return render(request, 'relationship_app/register.html', context)
# 

# --- 2. Login View (Class-Based - using Django's built-in) ---

class CustomLoginView(LoginView):
    """Custom LoginView to specify the template."""
    # Specifies the template to use
    template_name = 'relationship_app/login.html'
    
    # Specifies where to go after a successful login (using the corrected name 'book-list')
    next_page = reverse_lazy('relationship_app:book-list')


# --- 3. Logout View (Class-Based - using Django's built-in) ---

class CustomLogoutView(LogoutView):
    """Custom LogoutView to specify the template."""
    # Specifies the template to display after logout (logout.html)
    template_name = 'relationship_app/logout.html'
    # Optional: Redirects to the login page after the logout template is rendered
    next_page = reverse_lazy('relationship_app:login')