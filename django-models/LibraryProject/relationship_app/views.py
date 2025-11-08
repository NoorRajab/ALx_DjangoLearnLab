# relationship_app/views.py
from django.shortcuts import render
from django.views.generic.detail import DetailView # Previous correction retained
from .models import Library, Book
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test # NEW IMPORT!
from django.contrib.auth.views import LoginView, LogoutView # Built-in auth views
from django.contrib.auth.forms import UserCreationForm # Form for registration
from django.contrib.auth import login
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .models import Book, Library, UserProfile # Import UserProfile

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

def is_admin(user):
    """Checks if the user has the 'Admin' role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.ADMIN

def is_librarian(user):
    """Checks if the user has the 'Librarian' role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.LIBRARIAN

def is_member(user):
    """Checks if the user has the 'Member' role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.MEMBER


# --- Role-Based Views ---

# The login_url directs the user to the login page if the test fails.
@user_passes_test(is_admin, login_url='/relationship/login/')
def admin_view(request):
    """View accessible only to Admin users."""
    context = {'message': 'Welcome, Admin! You have full system access.'}
    return render(request, 'relationship_app/admin_view.html', context)

@user_passes_test(is_librarian, login_url='/relationship/login/')
def librarian_view(request):
    """View accessible only to Librarian users."""
    # Example: Query all books
    books = Book.objects.all().select_related('author')
    context = {'books': books, 'message': 'Welcome, Librarian! You can manage books and libraries.'}
    return render(request, 'relationship_app/librarian_view.html', context)

@user_passes_test(is_member, login_url='/relationship/login/')
def member_view(request):
    """View accessible only to Member users."""
    # Example: Query the top 5 books
    top_books = Book.objects.all().order_by('-id')[:5]
    context = {'top_books': top_books, 'message': 'Welcome, Member! Enjoy browsing our resources.'}
    return render(request, 'relationship_app/member_view.html', context)