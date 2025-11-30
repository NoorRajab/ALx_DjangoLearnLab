# api/urls.py
from django.urls import path
from .views import (
    BookListView, 
    BookDetailView, 
    BookCreateView, 
    BookUpdateView, 
    BookDeleteView
)

urlpatterns = [
    # ListView: /api/books/list/ (GET)
    path('books/list/', BookListView.as_view(), name='book-list'),

    # DetailView: /api/books/detail/<int:pk>/ (GET)
    path('books/detail/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # CreateView: /api/books/create/ (POST)
    path('books/create/', BookCreateView.as_view(), name='book-create'),

    # UpdateView: /api/books/update/<int:pk>/ (PUT/PATCH)
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),

    # DeleteView: /api/books/delete/<int:pk>/ (DELETE)
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]

# Documentation Requirements (Step 6):
# The URL patterns are non-standard RESTful, explicitly defining the action (e.g., 'create', 'update', 'delete') 
# within the path, thereby requiring five separate endpoints to manage the Book resource.