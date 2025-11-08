# relationship_app/urls.py
from django.urls import path
from . import views
# CORRECTED: Importing the renamed function 'list_books'
from .views import list_books, LibraryDetailView 
from .views import register_view, CustomLoginView, CustomLogoutView
# Define the app namespace
app_name = 'relationship_app'

urlpatterns = [
    # 1. Route for Function-based View (Book List)
    # CORRECTED: Referencing the renamed function 'list_books'
    path('books/', list_books, name='book-list'), 
    
    # 2. Route for Class-based View (Library Detail)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    # 1. Registration
    path('register/', register_view, name='register'),
    
    # 2. Login
    path('login/', CustomLoginView.as_view(), name='login'),
    
    # 3. Logout
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]