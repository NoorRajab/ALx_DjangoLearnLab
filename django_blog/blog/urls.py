
from django.urls import path
from django.contrib.auth import views as auth_views # Import built-in views
from . import views

urlpatterns = [
    # ----------------
    # Core Blog Views (Placeholder)
    # ----------------
    path('', views.home, name='home'),
    
    # ----------------
    # Custom Authentication Views
    # ----------------
    # Custom Registration View
    path('register/', views.register_user, name='register'),
    # Custom Profile View (View & Edit)
    path('profile/', views.profile_view, name='profile'),
    
    # ----------------
    # Built-in Auth Views Overrides/Mappings
    # ----------------
    # Custom template for Login (Overriding the one in 'auth/')
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    # Logout View (Redirects to home by default, or settings.LOGOUT_REDIRECT_URL)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Password Reset/Change URLs (included via 'auth/')
    # e.g., /auth/password_change/ -> password_change
    # e.g., /auth/password_reset/ -> password_reset
]

# Set the LOGIN_REDIRECT_URL and LOGOUT_REDIRECT_URL in settings.py for consistency:
# LOGIN_REDIRECT_URL = 'profile'
# LOGOUT_REDIRECT_URL = 'home'