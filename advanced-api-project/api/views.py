
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# --- View Configurations ---

class BookListCreate(generics.ListCreateAPIView):
    """
    ListCreateAPIView combines the ListModelMixin and CreateModelMixin.

    Objective:
    - GET: List all books (List View).
    - POST: Create a new book (Create View).

    Permissions:
    - Read (GET) is allowed for everyone (AllowAny).
    - Write (POST) is restricted to authenticated users (IsAuthenticatedOrReadOnly).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Custom Permissions: Allow read access to anyone, but only authenticated users can create.
    # Note: DRF checks permissions sequentially. IsAuthenticatedOrReadOnly grants read access to all,
    # but only write access to authenticated users.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Customization Hook: 
    # Overriding perform_create to automatically set the author field based on the request user
    # (although our model links Book to Author, not User, this is a common customization pattern).
    # For simplicity, we'll ensure the serializer is ready to handle this foreign key.
    # (The BookSerializer was already set to read_only_fields = ['author'], 
    # so we'd need to adjust that for a real-world auto-assignment, but for this task, 
    # we'll keep the required fields simple and rely on the frontend to supply the 'author' ID.)

    # A customization to show only books published in a certain year, for example:
    # def get_queryset(self):
    #     year = self.request.query_params.get('year', None)
    #     if year is not None:
    #         return Book.objects.filter(publication_year=year)
    #     return Book.objects.all()


class BookDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView combines RetrieveModelMixin, UpdateModelMixin, and DestroyModelMixin.

    Objective:
    - GET: Retrieve a single book (Detail View).
    - PUT/PATCH: Update an existing book (Update View).
    - DELETE: Delete a book (Delete View).

    Permissions:
    - Read (GET) is allowed for everyone (AllowAny).
    - Write (PUT/PATCH/DELETE) is restricted to authenticated users (IsAuthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Custom Permissions: Allow read access to anyone, but only authenticated users can modify/delete.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Customization Example:
    # Ensure update/delete operations are only performed by the book's creator 
    # (Requires adding a 'user' field to the Book model, not implemented here, 
    # but the custom permission class would be used here, e.g., permissions.IsOwnerOrReadOnly).