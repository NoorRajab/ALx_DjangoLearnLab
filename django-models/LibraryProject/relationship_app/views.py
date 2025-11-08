# relationship_app/views.py
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView
from .models import Book, Library

def book_list_view(request):
    """
    Function-based view to list all books.
    Renders 'relationship_app/list_books.html'
    """
  
    all_books = Book.objects.all().select_related('author')
    
    context = {
        'books': all_books,
    }
    
    
    return render(request, 'relationship_app/list_books.html', context)



class LibraryDetailView(DetailView):
    """
    Class-based view (DetailView) to show details for a specific library.
    Automatically looks for a template named 'relationship_app/library_detail.html'
    """
   
    model = Library
    
   
    template_name = 'relationship_app/library_detail.html'
    
  
    context_object_name = 'library' 
    
    
    def get_queryset(self):
       
        return Library.objects.all().prefetch_related('books__author')

    