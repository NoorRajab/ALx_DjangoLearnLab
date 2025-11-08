# relationship_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

# CORRECTION APPLIED: Explicitly importing permission_required
from django.contrib.auth.decorators import user_passes_test, permission_required 
from django.contrib.auth.views import LoginView, LogoutView 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login

# Import the base forms for quick use
from django.forms import modelform_factory

# Import models
from .models import Book, Library, UserProfile, Author 


# --- Existing Views from Previous Tasks ---

def list_books(request):
    """Function-based view to list all books. (Name corrected previously)"""
    all_books = Book.objects.all().select_related('author')
    context = {'books': all_books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    """Class-based view to show details for a specific library. (Import corrected previously)"""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library' 
    def get_queryset(self):
        return Library.objects.all().prefetch_related('books__author')

def register_view(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:book-list')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# --- Role Check Helper Functions (from Task 3) ---

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.ADMIN

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.LIBRARIAN

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.MEMBER


# --- Role-Based Views (from Task 3) ---

@user_passes_test(is_admin, login_url='/relationship/login/')
def admin_view(request):
    context = {'message': 'Welcome, Admin! You have full system access.'}
    return render(request, 'relationship_app/admin_view.html', context)

@user_passes_test(is_librarian, login_url='/relationship/login/')
def librarian_view(request):
    books = Book.objects.all().select_related('author')
    context = {'books': books, 'message': 'Welcome, Librarian! You can manage books and libraries.'}
    return render(request, 'relationship_app/librarian_view.html', context)

@user_passes_test(is_member, login_url='/relationship/login/')
def member_view(request):
    top_books = Book.objects.all().order_by('-id')[:5]
    context = {'top_books': top_books, 'message': 'Welcome, Member! Enjoy browsing our resources.'}
    return render(request, 'relationship_app/member_view.html', context)


# --- Secured Book Management Views (from Task 4) ---

BookForm = modelform_factory(Book, fields=('title', 'author'))

# 1. Add Book (Requires 'can_add_book' permission)
@permission_required('relationship_app.can_add_book', login_url='/relationship/login/', raise_exception=True)
def add_book(request):
    """Secured view for adding a new book."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:book-list')
    else:
        form = BookForm()
    
    context = {'form': form, 'action': 'Add'}
    return render(request, 'relationship_app/book_form.html', context)

# 2. Edit Book (Requires 'can_change_book' permission)
@permission_required('relationship_app.can_change_book', login_url='/relationship/login/', raise_exception=True)
def edit_book(request, pk):
    """Secured view for editing an existing book."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:book-list')
    else:
        form = BookForm(instance=book)
    
    context = {'form': form, 'action': 'Edit', 'book': book}
    return render(request, 'relationship_app/book_form.html', context)

# 3. Delete Book (Requires 'can_delete_book' permission)
@permission_required('relationship_app.can_delete_book', login_url='/relationship/login/', raise_exception=True)
def delete_book(request, pk):
    """Secured view for deleting a book."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app:book-list')
    
    context = {'book': book}
    return render(request, 'relationship_app/book_confirm_delete.html', context)