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
    # Define role choices
    ADMIN = 'Admin'
    LIBRARIAN = 'Librarian' # Adjusted to match the task requirement exactly
    MEMBER = 'Member'       # Adjusted to match the task requirement exactly
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (LIBRARIAN, 'Librarian'),
        (MEMBER, 'Member'),
    ]
    
    # One-to-one link to the built-in Django User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Role field, defaulting to 'Member'
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=MEMBER,
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# --- Signal for Automatic Profile Creation ---

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal function to automatically create a UserProfile when a new User is created
    and ensure the profile is saved when the User object is saved.
    """
    if created:
        # Create the profile, defaulting the role to 'Member'
        UserProfile.objects.create(user=instance)
    # Ensure profile is created if not already present (e.g., for existing users via admin shell)
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()