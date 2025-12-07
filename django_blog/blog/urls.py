# blog/urls.py (Updated - Only showing relevant parts)
# ... (All previous imports remain the same) ...
from .views import (
    # ... (Existing Post CRUD views) ...
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView
)

urlpatterns = [
    # ... (Existing Post List, Create, Detail, Update, Delete URLs) ...

    # ----------------
    # Comment URL Patterns
    # ----------------
    # Create Comment: Handles the form submission for a new comment
    path('post/<int:post_pk>/comment/new/', CommentCreateView.as_view(), name='comment_create'),
    
    # Update Comment: Allows editing a specific comment
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    
    # Delete Comment: Handles comment deletion
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # ... (Existing Authentication URLs) ...
]