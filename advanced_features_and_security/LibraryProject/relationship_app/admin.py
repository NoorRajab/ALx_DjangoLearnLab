

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

# Define a custom Admin class for the CustomUser model
class CustomUserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # We include 'email', and the new custom field 'date_of_birth'
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')
    
    # Custom fields must be added to a fieldset for display in the forms.
    # We modify the existing 'Personal Info' fieldset to include our custom fields.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Add new fields to be searched (if necessary)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    # We remove the default 'username' fields from add_fieldsets as well
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
    )

# Unregister the default User and register the CustomUser with the custom admin class
# The built-in User is usually not registered if you are using a custom model
admin.site.register(CustomUser, CustomUserAdmin)