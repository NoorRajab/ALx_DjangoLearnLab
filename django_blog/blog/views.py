# blog/views.py (Updated)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
# ... other imports (register_user, profile_view, CustomUserCreationForm) ...

from .models import Post
from .forms import PostForm # We will define this PostForm next

# ----------------------------------------------------
# 1. READ Operations (Accessible to all users)
# ----------------------------------------------------

class PostListView(ListView):
    """Displays a list of all published blog posts."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts' # Name of the list variable in the template
    ordering = ['-published_date'] # Order by newest first

class PostDetailView(DetailView):
    """Displays a single blog post."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# ----------------------------------------------------
# 2. CREATE Operation (Requires login)
# ----------------------------------------------------

class PostCreateView(LoginRequiredMixin, CreateView):
    """Allows authenticated users to create a new post."""
    model = Post
    form_class = PostForm # Use the ModelForm we define in forms.py
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Automatically set the author before saving the form."""
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    # Define where to go after successful creation
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

# ----------------------------------------------------
# 3. UPDATE Operation (Requires login and author check)
# ----------------------------------------------------

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows the post author to edit their existing post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        """Check if the logged-in user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author
        
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

# ----------------------------------------------------
# 4. DELETE Operation (Requires login and author check)
# ----------------------------------------------------

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows the post author to delete their post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    # Define where to go after successful deletion
    success_url = reverse_lazy('post_list') 
    
    def test_func(self):
        """Check if the logged-in user is the author of the post."""
        post = self.get_object()
        return self.request.user == post.author

# --- Placeholder/Existing Views ---
# Note: Rename the previous 'home' view to 'post_list' to align with CBVs.
# def home(request):
#     return render(request, 'blog/post_list.html', {'posts': Post.objects.all()[:5]})