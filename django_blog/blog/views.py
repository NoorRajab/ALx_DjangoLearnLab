# blog/views.py (Updated - Only showing new/modified views)
# ... (All previous imports remain the same) ...
from django.db.models import Q # Import Q object for complex lookups
from taggit.models import Tag

# ----------------------------------------------------
# 1. Search Functionality View
# ----------------------------------------------------

class PostSearchView(ListView):
    """Handles searching posts by title, content, and tags."""
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q') # Get the search query from the URL
        
        if query:
            # 1. Look up by Title or Content
            # Q objects allow OR lookups (combining different fields with OR | )
            object_list = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).distinct()
            
            # 2. Add Tag Search: Filter by posts that have a tag matching the query
            tag_posts = Post.objects.filter(tags__name__icontains=query).distinct()
            
            # Combine the results and ensure uniqueness
            return (object_list | tag_posts).order_by('-published_date')
        
        # If no query, return an empty set or a default list
        return Post.objects.none() 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

# ----------------------------------------------------
# 2. Tag Filtering View
# ----------------------------------------------------

class PostTagListView(ListView):
    """Displays posts associated with a specific tag name."""
    model = Post
    template_name = 'blog/post_list_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Get the tag name from the URL path (slug is used for tag names)
        tag_slug = self.kwargs.get('tag_slug')
        
        if tag_slug:
            # Filter posts that have a tag with the given slug
            queryset = Post.objects.filter(tags__slug=tag_slug).order_by('-published_date')
            return queryset
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the actual Tag object to display its name in the template
        tag_slug = self.kwargs.get('tag_slug')
        context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context