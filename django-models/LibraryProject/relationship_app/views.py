# relationship_app/views.py
from django.shortcuts import render
from django.views.generic.detail import DetailView # Previous correction retained
from .models import Library, Book

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