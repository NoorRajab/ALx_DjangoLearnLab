
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm # Import our custom form
from .models import Post # Assuming Post model is still here

# ----------------
# Registration View
# ----------------
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Force the email field to be saved on the user object
            user.email = form.cleaned_data.get('email')
            user.save()
            
            login(request, user) # Automatically log the user in after registration
            messages.success(request, "Registration successful. Welcome!")
            return redirect('profile') # Redirect to the profile page
        else:
            # Add form errors to messages for display in the template
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'blog/register.html', {'form': form})

# ----------------
# Profile View (View & Edit)
# ----------------
@login_required # Restrict access to logged-in users only
def profile_view(request):
    if request.method == 'POST':
        # Use the built-in UserChangeForm or a custom form for robust editing.
        # For simplicity, we'll handle basic User model fields directly here.
        
        # Security: Only update fields if they are present in the POST data
        if 'first_name' in request.POST:
            request.user.first_name = request.POST['first_name']
        if 'last_name' in request.POST:
            request.user.last_name = request.POST['last_name']
        if 'email' in request.POST:
            request.user.email = request.POST['email']
        
        request.user.save()
        messages.success(request, "Your profile has been updated successfully!")
        return redirect('profile') # Refresh the profile page
        
    context = {
        'user': request.user,
        # In a real app, you'd use a form here, e.g., UserChangeForm, for validation
    }
    return render(request, 'blog/profile.html', context)
    
# --- Placeholder for Home View (Assuming it exists for redirection) ---
def home(request):
    # This is a placeholder for your main blog view
    # You might want to filter posts by published=True, etc.
    context = {
        'posts': Post.objects.all()[:5]
    }
    return render(request, 'blog/post_list.html', context)