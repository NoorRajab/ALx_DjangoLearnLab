# relationship_app/views.py
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library, Book

# --- 1. Implement Function-based View ---

def book_list_view(request):
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
# 

# --- 2. Implement Class-based View (DetailView) ---

class LibraryDetailView(DetailView):
    """
    Class-based view (DetailView) to show details for a specific library.
    This view automatically handles fetching a single object based on the URL's primary key (pk).
    """
    # Specify the model to work with
    model = Library
    
    # Specify the template name, which will be searched inside the 'relationship_app/templates/relationship_app/' folder
    template_name = 'relationship_app/library_detail.html'
    
    # Specify the context object name (accessible in the template as 'library')
    context_object_name = 'library' 
    
    # Optional: Override get_queryset for query optimization
    def get_queryset(self):
        # Prefetch the related books and their authors to minimize database hits (N+1 problem)
        return Library.objects.all().prefetch_related('books__author')