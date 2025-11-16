
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.db.models import Q 
from .models import Book 
from .forms import ExampleForm, BookForm

@login_required 
@permission_required('users.can_view', raise_exception=True)
def book_list_view(request):

    books = Book.objects.all()
    can_create = request.user.has_perm('users.can_create')
    can_edit = request.user.has_perm('users.can_edit')
    can_delete = request.user.has_perm('users.can_delete')
    
    context = {
        'books': books,
        'can_create': can_create,
        'can_edit': can_edit,
        'can_delete': can_delete
    }
    return render(request, 'bookshelf/book_list.html', context)


@login_required
@permission_required('users.can_create', raise_exception=True)
def book_create_view(request):
   
    if request.method == 'POST':
        
        form = ExampleForm(request.POST) 
        if form.is_valid():
            
            feedback = form.cleaned_data['user_feedback']
            rating = form.cleaned_data['rating']
            
            print(f"Received Feedback: {feedback}, Rating: {rating}") 

            
            return redirect('book_list')
    else:
        form = ExampleForm()
        
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Submit Example'})


@login_required
@permission_required('users.can_edit', raise_exception=True)
def book_edit_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
        
    return render(request, 'bookshelf/book_form.html', {'form': form, 'book': book, 'action': 'Edit'})


@login_required
@permission_required('users.can_delete', raise_exception=True)
def book_delete_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
        
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


@login_required 
@permission_required('users.can_view', raise_exception=True)
def book_search_view(request):
    search_query = request.GET.get('q', '')
    books = Book.objects.none() 

    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query)
        ).distinct()

    return render(request, 'bookshelf/book_search.html', {
        'books': books,
        'search_query': search_query
    })