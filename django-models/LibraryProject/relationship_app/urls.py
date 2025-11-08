# relationship_app/urls.py
from django.urls import path
from . import views
# CORRECTION APPLIED: Explicitly importing the function-based view
from .views import book_list_view, LibraryDetailView # Combined imports for clarity

# Define the app namespace (useful for {% url 'relationship_app:...' %} template tags)
app_name = 'relationship_app'

urlpatterns = [
    # 1. Route for Function-based View (Book List)
    # Using the explicitly imported view function
    path('books/', book_list_view, name='book-list'),
    
    # 2. Route for Class-based View (Library Detail)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]