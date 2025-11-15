

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model # Utility for Step 5 update

# --- Custom User Manager (Step 3) ---
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a CustomUser with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
            
        return self.create_user(email, password, **extra_fields)


# --- Custom User Model (Step 1) ---
class CustomUser(AbstractUser):
    # Overriding the default username field
    username = None 
    email = models.EmailField(_('email address'), unique=True)
    
    # Custom Fields to Add
    date_of_birth = models.DateField(
        _('date of birth'),
        null=True, 
        blank=True
    )
    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to='profile_photos/', 
        null=True, 
        blank=True
    )

    # Use email for the unique identifier (login field)
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS are fields prompted when using createsuperuser
    REQUIRED_FIELDS = ['first_name', 'last_name'] 

    # Assign the custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.email

# --- Existing Application Model (Step 5 Update) ---
# Note: Since the original Book model did not have a ForeignKey to User, 
# no change is strictly required for Book, but if it did, this is how you'd update it.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    
    publication_year = models.IntegerField()
    # If the Book model needed to reference a user, the change would look like this:
    # added_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='books_added')

    def __str__(self):
        return f"{self.title} by {self.author}"