
from django.contrib import admin
from django.urls import path, include
from blog.views import home # Import placeholder home view

urlpatterns = [
    path('admin/', admin.site.urls),
    # Use include() for the main blog app's URLs
    path('', include('blog.urls')), 
    # Use include() for Django's built-in authentication URLs
    # This automatically includes paths like login/, logout/, password_change/, etc.
    # We map them to the root /auth/ or simply use the built-in names
    path('auth/', include('django.contrib.auth.urls')), 
]