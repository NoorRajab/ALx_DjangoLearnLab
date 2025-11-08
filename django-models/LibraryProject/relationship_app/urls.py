# relationship_app/urls.py
from django.urls import path
from . import views
# CORRECTED: Importing the renamed function 'list_books'
from .views import list_books, LibraryDetailView 

# Define the app namespace
app_name = 'relationship_app'

urlpatterns = [
    # 1. Route for Function-based View (Book List)
    # CORRECTED: Referencing the renamed function 'list_books'
    path('books/', list_books, name='book-list'), 
    
    # 2. Route for Class-based View (Library Detail)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]