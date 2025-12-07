from django.db import models
from django.contrib.auth.models import User # Import Django's built-in User model

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    # ForeignKey to Django's User model, on_delete=models.CASCADE means 
    # posts are deleted if the author (User) is deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title # A readable representation of the object