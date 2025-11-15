# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Book

# --- Custom User Admin (Step 4) ---
class CustomUserAdmin(BaseUserAdmin):
    # Fields to display in the list view
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')
    
    # Fields in the edit form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}), # Includes new fields
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'first_name', 'last_name', 'date_of_birth', 'profile_photo'),
        }),
    )
    
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)

# --- Existing Book Admin ---
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')

    ordering = ('-publication_year',)

admin.site.register(Book, BookAdmin)