from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} by {self.author.name}"

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Librarian {self.name} at {self.library.name}"

class UserProfile(models.Model):
  
    ADMIN = 'Admin'
    LIBRARIAN = 'Librarian' 
    MEMBER = 'Member'       
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (LIBRARIAN, 'Librarian'),
        (MEMBER, 'Member'),
    ]
    
   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=MEMBER,
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    
    if created:
        
        UserProfile.objects.create(user=instance)
    
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

class Book(models.Model):
    title = models.CharField(max_length=200)
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    
    class Meta:
        permissions = [
            
            ("can_add_book", "Can add new books to the catalog"),
            ("can_change_book", "Can edit existing book details"),
            ("can_delete_book", "Can delete books from the catalog"),
        ]

