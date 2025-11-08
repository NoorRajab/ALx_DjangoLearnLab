
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login
from django.forms import modelform_factory
from .models import Book, Library, UserProfile, Author 


def list_books(request):
    
    all_books = Book.objects.all().select_related('author')
    context = {'books': all_books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library' 
    def get_queryset(self):
        return Library.objects.all().prefetch_related('books__author')

def register_view(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:book-list')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.ADMIN

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.LIBRARIAN

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.MEMBER



@user_passes_test(is_admin, login_url='/relationship/login/')
def admin_view(request):
    context = {'message': 'Welcome, Admin! You have full system access.'}
    return render(request, 'relationship_app/admin_view.html', context)

@user_passes_test(is_librarian, login_url='/relationship/login/')
def librarian_view(request):
    books = Book.objects.all().select_related('author')
    context = {'books': books, 'message': 'Welcome, Librarian! You can manage books and libraries.'}
    return render(request, 'relationship_app/librarian_view.html', context)

@user_passes_test(is_member, login_url='/relationship/login/')
def member_view(request):
    top_books = Book.objects.all().order_by('-id')[:5]
    context = {'top_books': top_books, 'message': 'Welcome, Member! Enjoy browsing our resources.'}
    return render(request, 'relationship_app/member_view.html', context)


BookForm = modelform_factory(Book, fields=('title', 'author'))


@permission_required('relationship_app.can_add_book', login_url='/relationship/login/', raise_exception=True)
def add_book(request):
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:book-list')
    else:
        form = BookForm()
    
    context = {'form': form, 'action': 'Add'}
    return render(request, 'relationship_app/book_form.html', context)

@permission_required('relationship_app.can_change_book', login_url='/relationship/login/', raise_exception=True)
def edit_book(request, pk):
    """Secured view for editing an existing book."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:book-list')
    else:
        form = BookForm(instance=book)
    
    context = {'form': form, 'action': 'Edit', 'book': book}
    return render(request, 'relationship_app/book_form.html', context)

@permission_required('relationship_app.can_delete_book', login_url='/relationship/login/', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app:book-list')
    
    context = {'book': book}
    return render(request, 'relationship_app/book_confirm_delete.html', context)