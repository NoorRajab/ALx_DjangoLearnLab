
from django.urls import path
from .views import BookListCreate, BookDetailUpdateDelete

# The urlpatterns connect the URLs to the views.
urlpatterns = [
    # Endpoint: /api/books/
    # Handled by BookListCreate: GET (List all books) and POST (Create new book)
    path('books/', BookListCreate.as_view(), name='book-list-create'),

    # Endpoint: /api/books/<int:pk>/
    # Handled by BookDetailUpdateDelete: GET (Retrieve), PUT/PATCH (Update), DELETE (Destroy)
    # The <int:pk> is a keyword argument passed to the view to identify the specific object.
    path('books/<int:pk>/', BookDetailUpdateDelete.as_view(), name='book-detail-update-delete'),
]

# Documentation Requirements:
# The URL patterns provide clear, semantic paths for resource access.
# - The list/create view is mapped to the plural noun ('books/').
# - The detail/update/delete view is mapped to the plural noun plus a primary key identifier ('books/<int:pk>/').