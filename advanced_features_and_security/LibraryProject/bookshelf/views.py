# LibraryProject/bookshelf/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.db.models import Q # Used for secure search demonstration
from .models import Book 
# IMPORTANT: Updated import to include ExampleForm
from .forms import ExampleForm, BookForm


# The application name is assumed to be 'bookshelf' for permission checks
# However, permissions were previously defined using 'users', 
# so 'users' is retained here for consistency with previous steps.

@login_required 
@permission_required('users.can_view', raise_exception=True)
def book_list_view(request):
    """
    Displays the list of books. Requires 'can_view' permission.
    Security Rationale: Uses Django ORM (objects.all()) to prevent SQL Injection.
    """
    books = Book.objects.all()
    # Check for additional permissions to control template display
    can_create = request.user.has_perm('users.can_create')
    can_edit = request.user.has_perm('users.can_edit')
    can_delete = request.user.has_perm('users.can_delete')
    
    context = {
        'books': books,
        'can_create': can_create,
        'can_edit': can_edit,
        'can_delete': can_delete
    }
    return render(request, 'bookshelf/book_list.html', context)


@login_required
@permission_required('users.can_create', raise_exception=True)
def book_create_view(request):
    """
    Handles form submission for a new book using the ExampleForm for demonstration.
    Requires 'can_create' permission.
    """
    # NOTE: Using ExampleForm to meet the last user request.
    if request.method == 'POST':
        # Security Rationale: ExampleForm handles validation and sanitation of user input.
        form = ExampleForm(request.POST) 
        if form.is_valid():
            # Process non-model data manually
            feedback = form.cleaned_data['user_feedback']
            rating = form.cleaned_data['rating']
            
            # In a real app, this would process the non-book data (e.g., save feedback to a separate table)
            print(f"Received Feedback: {feedback}, Rating: {rating}") 

            # If you wanted to create a book here, you would use BookForm instead of ExampleForm:
            # BookForm(request.POST).save()

            # Redirect to a success page or the list view
            return redirect('book_list')
    else:
        # Use ExampleForm for display
        form = ExampleForm()
        
    # The template name should be updated to reflect the new project structure
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Submit Example'})


@login_required
@permission_required('users.can_edit', raise_exception=True)
def book_edit_view(request, pk):
    """
    Handles modifying an existing book. Requires 'can_edit' permission.
    """
    # Security Rationale: get_object_or_404 uses the ORM, preventing SQL Injection.
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # Security Rationale: BookForm handles validation and sanitation of user input.
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            # Security Rationale: form.save() uses the ORM, preventing SQL Injection.
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
        
    return render(request, 'bookshelf/book_form.html', {'form': form, 'book': book, 'action': 'Edit'})


@login_required
@permission_required('users.can_delete', raise_exception=True)
def book_delete_view(request, pk):
    """
    Handles deleting a book. Requires 'can_delete' permission.
    """
    # Security Rationale: get_object_or_404 uses the ORM, preventing SQL Injection.
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # Security Rationale: book.delete() uses the ORM, preventing SQL Injection.
        book.delete()
        return redirect('book_list')
        
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


@login_required 
@permission_required('users.can_view', raise_exception=True)
def book_search_view(request):
    """
    Securely handles user input for a search query using the Django ORM.
    This prevents SQL Injection.
    """
    search_query = request.GET.get('q', '')
    books = Book.objects.none() # Initialize an empty queryset

    if search_query:
        # Security Rationale: Uses the ORM's filtering methods (icontains) instead of 
        # string concatenation to safely handle and parameterize user input.
        books = Book.objects.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query)
        ).distinct()

    return render(request, 'bookshelf/book_search.html', {
        'books': books,
        'search_query': search_query
    })