from django.shortcuts import render
from models import Book
from .models import Library
from django.views.generic.detail import DetailView
# Create your views here.

def list_books(request):
    books = Book.objects.all()
    list = {'list_books' : books}
    return render(request, 'relationship_app/list_books.html',list)


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'