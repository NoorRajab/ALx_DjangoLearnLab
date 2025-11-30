# api/views.py
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

class BookListCreate(generics.ListCreateAPIView):
    """
    ListCreateAPIView combines:
    1. ListView (via ListModelMixin): Handles GET request to retrieve a list of books.
    2. CreateView (via CreateModelMixin): Handles POST request to create a new book.

    Permissions (Step 4):
    - permissions.IsAuthenticatedOrReadOnly: Allows unauthenticated users READ access (GET),
      but restricts WRITE access (POST) to authenticated users only.
    """
    # Required for List/Retrieve operations
    queryset = Book.objects.all()
    # Required for Serialization/Validation
    serializer_class = BookSerializer
    # Permission check implementation
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Customization Hook Example (Step 3):
    # This ensures any custom validation (like publication_year check in the serializer)
    # is executed during creation. The ListCreateAPIView handles this automatically,
    # but this is where further custom logic could be added, e.g., setting the author
    # based on the request user, if the models were set up for it.


class BookDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView combines:
    1. DetailView (via RetrieveModelMixin): Handles GET request to retrieve a single book.
    2. UpdateView (via UpdateModelMixin): Handles PUT/PATCH request to update a book.
    3. DeleteView (via DestroyModelMixin): Handles DELETE request to remove a book.

    Permissions (Step 4):
    - permissions.IsAuthenticatedOrReadOnly: Allows unauthenticated users READ access (GET),
      but restricts WRITE/DELETE access (PUT, PATCH, DELETE) to authenticated users only.
    """
    # Required for Detail/Update/Delete operations
    queryset = Book.objects.all()
    # Required for Serialization/Validation
    serializer_class = BookSerializer
    # Permission check implementation
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Customization Hook Example (Step 3):
    # Overriding perform_update or perform_destroy is often done here 
    # to add logging or enforce business logic before modification/deletion.
    # The view correctly handles data validation automatically by using the serializer_class.