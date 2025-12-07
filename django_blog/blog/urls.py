
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    PostSearchView,
    PostTagListView,
)

urlpatterns = [
    # ----------------
    # Post CRUD URL Patterns
    # ----------------
    path('', PostListView.as_view(), name='post_list'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # ----------------
    # Advanced Feature URL Patterns
    # ----------------
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('tags/<slug:tag_slug>/', PostTagListView.as_view(), name='posts_by_tag'),

    # ----------------
    # Comment URL Patterns (FIXED)
    # ----------------
    # Create Comment: Uses 'post/<int:pk>/comments/new/'
    path('post/<int:post_pk>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    
    # Update Comment: Uses 'comment/<int:pk>/update/'
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    
    # Delete Comment (Remains the same path structure for consistency)
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # ----------------
    # Authentication URL Patterns
    # ----------------
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]