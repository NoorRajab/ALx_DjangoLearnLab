# api/views.py
from rest_framework import generics, permissions, mixins
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# Base class providing queryset and serializer context
class BookBaseView(generics.GenericAPIView):
    """Base class for Book operations, defining common settings."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Apply permissions to the base class: Read-Only for anyone, Write for authenticated.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# --- 1. ListView (GET list) ---
class BookListView(mixins.ListModelMixin, BookBaseView):
    """
    Handles GET request to list all Book instances.
    Equivalent to a traditional ListView.
    """
    def get(self, request, *args, **kwargs):
        # Calls the ListModelMixin's list() method
        return self.list(request, *args, **kwargs)


# --- 2. DetailView (GET retrieve) ---
class BookDetailView(mixins.RetrieveModelMixin, BookBaseView):
    """
    Handles GET request to retrieve a single Book instance by PK.
    Equivalent to a traditional DetailView.
    """
    def get(self, request, *args, **kwargs):
        # Calls the RetrieveModelMixin's retrieve() method
        return self.retrieve(request, *args, **kwargs)


# --- 3. CreateView (POST create) ---
class BookCreateView(mixins.CreateModelMixin, BookBaseView):
    """
    Handles POST request to create a new Book instance.
    Equivalent to a traditional CreateView.
    """
    # Customization Hook (Step 3): Permissions enforced via permission_classes on base view.
    # The CreateModelMixin handles validation via serializer_class automatically.
    def post(self, request, *args, **kwargs):
        # Calls the CreateModelMixin's create() method
        return self.create(request, *args, **kwargs)


# --- 4. UpdateView (PUT/PATCH update) ---
class BookUpdateView(mixins.UpdateModelMixin, BookBaseView):
    """
    Handles PUT/PATCH requests to update an existing Book instance by PK.
    Equivalent to a traditional UpdateView.
    """
    # Customization Hook (Step 3): Permissions enforced via permission_classes on base view.
    def put(self, request, *args, **kwargs):
        # Calls the UpdateModelMixin's update() method
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Calls the UpdateModelMixin's partial_update() method
        return self.partial_update(request, *args, **kwargs)


# --- 5. DeleteView (DELETE destroy) ---
class BookDeleteView(mixins.DestroyModelMixin, BookBaseView):
    """
    Handles DELETE request to destroy an existing Book instance by PK.
    Equivalent to a traditional DeleteView.
    """
    # Permissions (Step 4): Permissions enforced via permission_classes on base view.
    def delete(self, request, *args, **kwargs):
        # Calls the DestroyModelMixin's destroy() method
        return self.destroy(request, *args, **kwargs)