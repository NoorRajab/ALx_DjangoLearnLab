
from django.urls import path
from .views import BookListCreate, BookDetailUpdateDelete

# The urlpatterns connect the URLs to the views.
urlpatterns = [
    # Endpoint: /api/books/
    # Maps to ListCreateAPIView: Handles GET (List) and POST (Create)
    path('books/', BookListCreate.as_view(), name='book-list-create'),

    # Endpoint: /api/books/<int:pk>/
    # Maps to RetrieveUpdateDestroyAPIView: Handles GET (Detail), PUT/PATCH (Update), DELETE (Destroy)
    path('books/<int:pk>/', BookDetailUpdateDelete.as_view(), name='book-detail-update-delete'),
]

# Documentation Summary (Step 6):
# The URL structure is RESTful, using the plural noun '/books/' for the collection 
# and adding the primary key '/books/<int:pk>/' for a specific resource. 
# This ensures clear routing for all CRUD operations.