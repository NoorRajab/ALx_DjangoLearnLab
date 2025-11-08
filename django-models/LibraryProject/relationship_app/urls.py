# relationship_app/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView # NEW: Import built-in generic views directly
from . import views


# Previous corrections retained: Explicitly importing the function and class views
from .views import list_books, LibraryDetailView, register_view 

app_name = 'relationship_app'

urlpatterns = [
    # Existing General Views
    path('books/', list_books, name='book-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    
    # --- New Authentication Views (Corrected to use requested syntax) ---
    
    # 1. Registration
    # CORRECTED: Using 'views.register_view' via the imported 'views' namespace
    path('register/', views.register_view, name='register'),
    
    # 2. Login
    # CORRECTED: Using LoginView.as_view() with template_name specified
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # 3. Logout
    # CORRECTED: Using LogoutView.as_view() with template_name specified
    # Note: next_page is often used here but not explicitly requested, 
    # so we rely on the default or settings.LOGOUT_REDIRECT_URL.
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    # Admin Access
    path('admin-dashboard/', views.admin_view, name='admin-dashboard'),
    
    # Librarian Access
    path('librarian-panel/', views.librarian_view, name='librarian-panel'),
    
    # Member Access
    path('member-page/', views.member_view, name='member-page'),
    path('book/add/', views.add_book, name='book-add'),
    
    # Edit Book (Requires 'can_change_book')
    path('book/edit/<int:pk>/', views.edit_book, name='book-edit'),
    
    # Delete Book (Requires 'can_delete_book')
    path('book/delete/<int:pk>/', views.delete_book, name='book-delete'),
]