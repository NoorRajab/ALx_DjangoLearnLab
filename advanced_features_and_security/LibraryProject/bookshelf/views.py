# library_catalog/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from .models import Book
from .forms import BookForm # Assume you have a simple BookForm defined

# The application name is used in the permission string: 'app_name.permission_codename'

@login_required 
@permission_required('library_catalog.can_view', raise_exception=True)
def book_list_view(request):
    """
    Allows users with 'can_view' permission to see the book list.
    """
    books = Book.objects.all()
    return render(request, 'library_catalog/book_list.html', {'books': books})

@login_required
@permission_required('library_catalog.can_create', raise_exception=True)
def book_create_view(request):
    """
    Allows users with 'can_create' permission to add a new book.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library_catalog/book_form.html', {'form': form, 'action': 'Create'})

@login_required
@permission_required('library_catalog.can_edit', raise_exception=True)
def book_edit_view(request, pk):
    """
    Allows users with 'can_edit' permission to modify an existing book.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'library_catalog/book_form.html', {'form': form, 'book': book, 'action': 'Edit'})

@login_required
@permission_required('library_catalog.can_delete', raise_exception=True)
def book_delete_view(request, pk):
    """
    Allows users with 'can_delete' permission to remove a book.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    # Use a simple confirmation page template
    return render(request, 'library_catalog/book_confirm_delete.html', {'book': book})