# blog/views.py (Updated with login_required import)
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q 
from taggit.models import Tag
from django.contrib.auth.decorators import login_required # <--- ADDED IMPORT

# Import necessary forms and models
from .forms import PostForm, CommentForm, CustomUserCreationForm 
from .models import Post, Comment

# ----------------------------------------------------
# Function-Based Views (FBVs)
# ----------------------------------------------------

def register_user(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # Redirect to login page after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required # <--- Using the added decorator for profile access control
def profile_view(request):
    """Displays the user's profile and their posts."""
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    return render(request, 'blog/profile.html', {'user_posts': user_posts})

# ----------------------------------------------------
# Class-Based Views (CBVs) - Post CRUD
# ----------------------------------------------------

class PostListView(ListView):
    """Displays a list of all blog posts."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

class PostDetailView(DetailView):
    """Displays a single blog post and its comment form."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm() 
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """Allows authenticated users to create a new post."""
    model = Post
    form_class = PostForm 
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows the post author to edit their existing post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
        
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows the post author to delete their post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list') 
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# ----------------------------------------------------
# CBVs - Comment CRUD
# ----------------------------------------------------

class CommentCreateView(LoginRequiredMixin, CreateView):
    """Handles the submission of a new comment."""
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs.get('post_pk')})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows the comment author to edit their comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html' 

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows the comment author to delete their comment."""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
        
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

# ----------------------------------------------------
# CBVs - Search and Tagging
# ----------------------------------------------------

class PostSearchView(ListView):
    """Handles searching posts by title, content, and tags."""
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        
        if query:
            object_list = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).distinct()
            
            tag_posts = Post.objects.filter(tags__name__icontains=query).distinct()
            
            return (object_list | tag_posts).order_by('-published_date')
        
        return Post.objects.none() 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

class PostTagListView(ListView):
    """Displays posts associated with a specific tag name."""
    model = Post
    template_name = 'blog/post_list_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        
        if tag_slug:
            queryset = Post.objects.filter(tags__slug=tag_slug).order_by('-published_date')
            return queryset
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context