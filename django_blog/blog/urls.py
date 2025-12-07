# blog/urls.py (Updated)
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    # ----------------
    # CRUD URL Patterns
    # ----------------
    # Read: List of Posts
    path('', PostListView.as_view(), name='post_list'), # Home page is the post list
    
    # Create: New Post
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    
    # Read: Detail View (using the post's primary key <pk>)
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    
    # Update: Edit Post
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    
    # Delete: Delete Post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # ----------------
    # Authentication URL Patterns (from Task 1)
    # ----------------
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]