# relationship_app/urls.py
from django.urls import path
from . import views
from .views import LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
   
    path('books/', views.book_list_view, name='book-list'),
    
    
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]