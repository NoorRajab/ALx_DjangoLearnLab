# users/views.py (Updated with Documentation/Comments - Step 5)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from .models import Book 
from .forms import BookForm 
from django.db.models import Q # Included for demonstrating secure search

# The application name is 'users' based on where the models file is located.

@login_required 
@permission_required('users.can_view', raise_exception=True)
def book_list_view(request):
    """
    Displays the list of books. Requires 'can_view' permission.
    """
    # Security Rationale: Uses Django ORM (objects.all()) to prevent SQL Injection (Step 3)
    books = Book.objects.all()
    # Check for additional permissions to control what is displayed in the template (optional best practice)
    can_create = request.user.has_perm('users.can_create')
    can_edit = request.user.has_perm('users.can_edit')
    can_delete = request.user.has_perm('users.can_delete')
    
    context = {
        'books': books,
        'can_create': can_create,
        'can_edit': can_edit,
        'can_delete': can_delete
    }
    return render(request, 'users/book_list.html', context)


@login_required
@permission_required('users.can_create', raise_exception=True)
def book_create_view(request):
    """
    Handles adding a new book. Requires 'can_create' permission.
    """
    if request.method == 'POST':
        # Security Rationale: BookForm handles validation and sanitation of user input, 
        # preventing XSS before saving to the database (Step 3).
        form = BookForm(request.POST) 
        if form.is_valid():
            # Security Rationale: form.save() uses the ORM, preventing SQL Injection (Step 3).
            form.save() 
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'users/book_form.html', {'form': form, 'action': 'Create'})


@login_required
@permission_required('users.can_edit', raise_exception=True)
def book_edit_view(request, pk):
    """
    Handles modifying an existing book. Requires 'can_edit' permission.
    """
    # Security Rationale: get_object_or_404 uses the ORM, preventing SQL Injection (Step 3).
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # Security Rationale: BookForm handles validation and sanitation of user input (Step 3).
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            # Security Rationale: form.save() uses the ORM, preventing SQL Injection (Step 3).
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'users/book_form.html', {'form': form, 'book': book, 'action': 'Edit'})


@login_required
@permission_required('users.can_delete', raise_exception=True)
def book_delete_view(request, pk):
    """
    Handles deleting a book. Requires 'can_delete' permission.
    """
    # Security Rationale: get_object_or_404 uses the ORM, preventing SQL Injection (Step 3).
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # Security Rationale: book.delete() uses the ORM, preventing SQL Injection (Step 3).
        book.delete()
        return redirect('book_list')
    # Templates will ensure proper escaping of book.title to prevent XSS (default Django template behavior)
    return render(request, 'users/book_confirm_delete.html', {'book': book})