# blog/models.py (Updated)
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class Post(models.Model):
    # ... (existing Post model content remains the same) ...
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Good practice for CBVs to redirect after creation/update
        return reverse('post_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-published_date']


class Comment(models.Model):
    """Model to store user comments on blog posts."""
    # ForeignKey to the Post model, related_name allows easy access from Post: post.comments.all()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    
    # ForeignKey to the User model
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The actual comment content
    content = models.TextField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Order comments with the newest at the top
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title[:20]}...'
        
    def get_absolute_url(self):
        # Redirect back to the post detail page after comment creation/update/delete
        return reverse('post_detail', kwargs={'pk': self.post.pk})