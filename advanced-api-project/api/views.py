from django_filters import rest_framework
from rest_framework import generics, permissions
from rest_framework import filters  # Import the filters module
from django_filters.rest_framework import DjangoFilterBackend # Import the DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter # Import the custom filterset

class BookListCreate(generics.ListCreateAPIView):
    """
    ListCreateAPIView with Filtering, Searching, and Ordering enabled.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Define the filter backends to be used in this view
    filter_backends = [
        DjangoFilterBackend,       # Step 1: Enables comprehensive filtering
        filters.SearchFilter,      # Step 2: Enables text search
        filters.OrderingFilter,    # Step 3: Enables field ordering
    ]
    
    # Filtering Configuration (Step 1)
    # Use the custom FilterSet for advanced filtering logic
    filterset_class = BookFilter 

    # Search Configuration (Step 2)
    # Fields to search across (case-insensitive text search)
    search_fields = ['title', 'author__name'] # Search across Book title and the linked Author's name
    
    # Ordering Configuration (Step 3)
    # Fields available for ordering
    ordering_fields = ['title', 'publication_year', 'id']
    # Default ordering (e.g., by ID ascending)
    ordering = ['id'] 


# BookDetailUpdateDelete remains unchanged as these features only apply to list views.
class BookDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    # ... (code for BookDetailUpdateDelete remains the same)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]