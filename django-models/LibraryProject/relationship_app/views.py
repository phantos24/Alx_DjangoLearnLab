from django.shortcuts import render
from models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.urls import path
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import permission_required
# Create your views here.

def list_books(request):
    books = Book.objects.all()
    list = {'list_books' : books}
    return render(request, 'relationship_app/list_books.html',list)


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'

class SignUpView(CreateView):
    form_class = UserCreationForm()
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'


def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html',
    {'message' : "Welcome to Admin Dashboard"})

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html',
    {'message' : "Welcome to librarian View"})

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html',
    {'message' : "Welcome to member View"})

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_date = request.POST.get('publication_date')
        
        if not title or not author:
            return render(request, 'add_book.html', {'error': 'Title and Author are required.'})
        
        Book.objects.create(title=title, author=author, publication_date=publication_date)
        return redirect('book_list')
    
    return render(request, 'add_book.html')

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    if not request.user.has_perm('bookshelf.can_change_book'):
        return HttpResponseForbidden("You do not have permission to edit this book.")
    
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_date = request.POST.get('publication_date')

        if not title or not author:
            return render(request, 'edit_book.html', {'book': book, 'error': 'Title and Author are required.'})
        
        book.title = title
        book.author = author
        book.publication_date = publication_date
        book.save()

        return redirect('book_list')

    return render(request, 'edit_book.html', {'book': book})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    if not request.user.has_perm('bookshelf.can_delete_book'):
        return HttpResponseForbidden("You do not have permission to delete this book.")
    
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')

    return render(request, 'confirm_delete_book.html', {'book': book})
