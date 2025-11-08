# relationship_app/urls.py
from django.urls import path
from . import views
from .views import LibraryDetailView, CustomLoginView, CustomLogoutView # Import the custom auth views

app_name = 'relationship_app'

urlpatterns = [
    # Existing Views from previous task
    path('books/', views.book_list_view, name='book-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    
    # --- New Authentication Views ---
    
    # 1. Registration
    path('register/', views.register_view, name='register'),
    
    # 2. Login (Uses the CustomLoginView class's .as_view() method)
    path('login/', CustomLoginView.as_view(), name='login'),
    
    # 3. Logout (Uses the CustomLogoutView class's .as_view() method)
    # The default behavior of LogoutView is to log the user out and then render the template specified by template_name.
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]