# relationship_app/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView 
from . import views

# Previous corrections retained: Explicitly importing core app views
from .views import list_books, LibraryDetailView, register_view 

# CORRECTION APPLIED: Explicitly importing all book management views
from .views import admin_view, librarian_view, member_view, add_book, edit_book, delete_book

app_name = 'relationship_app'

urlpatterns = [
    # Existing General/Auth Views
    path('books/', list_books, name='book-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # Existing RBAC Views
    path('admin-dashboard/', views.admin_view, name='admin-dashboard'),
    path('librarian-panel/', views.librarian_view, name='librarian-panel'),
    path('member-page/', views.member_view, name='member-page'),

    # --- Secured Book Management URLs (Corrected to use explicit imports) ---
    
    # Add Book (Requires 'can_add_book')
    path('book/add/', add_book, name='book-add'), # Using explicitly imported view
    
    # Edit Book (Requires 'can_change_book')
    path('book/edit/<int:pk>/', edit_book, name='book-edit'), # Using explicitly imported view
    
    # Delete Book (Requires 'can_delete_book')
    path('book/delete/<int:pk>/', delete_book, name='book-delete'), # Using explicitly imported view
]