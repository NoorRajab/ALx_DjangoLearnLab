# blog/views.py (Updated - Only showing new/modified views)
# ... (All previous imports remain the same) ...
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView # Import DetailView for use below
# ... (All Mixins and Model imports remain the same) ...
from django.urls import reverse_lazy

from .models import Post, Comment
from .forms import PostForm, CommentForm # Import CommentForm

# ----------------------------------------------------
# Modified: Post Detail View (To display comments and form)
# ----------------------------------------------------

class PostDetailView(DetailView):
    """Displays a single blog post and its comments, passing the comment form."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the CommentForm to the detail view context
        context['comment_form'] = CommentForm() 
        return context

# ----------------------------------------------------
# 1. CREATE Comment (Only for logged-in users)
# ----------------------------------------------------

class CommentCreateView(LoginRequiredMixin, CreateView):
    """Handles the submission of a new comment."""
    model = Comment
    form_class = CommentForm
    
    # We do not need a template; it handles the form submission from PostDetailView
    def form_valid(self, form):
        # 1. Set the Post based on the URL parameter (passed as post_pk)
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        form.instance.post = post
        
        # 2. Set the Author
        form.instance.author = self.request.user
        
        return super().form_valid(form)
    
    # Redirect back to the post detail page
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs.get('post_pk')})

# ----------------------------------------------------
# 2. UPDATE Comment (Requires login and author check)
# ----------------------------------------------------

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows the comment author to edit their comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html' # Use a dedicated template for editing

    def test_func(self):
        """Check if the logged-in user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author

    # Redirect back to the post detail page after update
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

# ----------------------------------------------------
# 3. DELETE Comment (Requires login and author check)
# ----------------------------------------------------

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows the comment author to delete their comment."""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        """Check if the logged-in user is the author of the comment."""
        comment = self.get_object()
        return self.request.user == comment.author
        
    # Redirect back to the post detail page after deletion
    def get_success_url(self):
        # The post primary key is available via the deleted object's instance
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})