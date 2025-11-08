
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView 
from . import views


from .views import list_books, LibraryDetailView, register_view 

from .views import admin_view, librarian_view, member_view, add_book, edit_book, delete_book

app_name = 'relationship_app'

urlpatterns = [
    path('books/', list_books, name='book-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    path('admin-dashboard/', views.admin_view, name='admin-dashboard'),
    path('librarian-panel/', views.librarian_view, name='librarian-panel'),
    path('member-page/', views.member_view, name='member-page'),

    path('book/add/', add_book, name='book-add'), 
    path('book/edit/<int:pk>/', edit_book, name='book-edit'), 
    path('book/delete/<int:pk>/', delete_book, name='book-delete'), 
]