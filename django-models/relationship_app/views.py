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
from django.shortcuts import render
from django.http import HttpResponse
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

