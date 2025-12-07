# blog/urls.py (Corrected)
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
    
    # FIX: Changed the path from 'edit/' to 'update/' as requested,
    # but kept the descriptive name 'post_update'.
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # ----------------
    # Advanced Feature URL Patterns
    # ----------------
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('tags/<slug:tag_slug>/', PostTagListView.as_view(), name='posts_by_tag'),

    # ----------------
    # Comment URL Patterns
    # ----------------
    path('post/<int:post_pk>/comment/new/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # ----------------
    # Authentication URL Patterns
    # ----------------
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]