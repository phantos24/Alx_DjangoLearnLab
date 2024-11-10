from django.shortcuts import render
from models import Book,Library
from django.views.generic import DetailView
# Create your views here.

def book_list(request):
    books = Book.objects.all()
    list = {'book_list' : books}
    return render(request, 'relationship_app/list_books.html',list)


class LibraryView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'