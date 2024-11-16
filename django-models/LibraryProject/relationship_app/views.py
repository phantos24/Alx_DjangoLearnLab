from django.shortcuts import render
from models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import path
# Create your views here.

def list_books(request):
    books = Book.objects.all()
    list = {'list_books' : books}
    return render(request, 'relationship_app/list_books.html',list)


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/signup.html'

urlpatterns = [
    login('view.register',LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
]

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
]