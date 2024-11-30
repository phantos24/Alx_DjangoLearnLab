from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book
from django.urls import reverse_lazy

# Create your views here.
class ListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

class DetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

class CreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'publication_year']  
    template_name = 'book_form.html'  
    success_url = reverse_lazy('book-list')  

class UpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'publication_year']  
    template_name = 'book_form.html'  
    success_url = reverse_lazy('book-list') 

class DeleteView(DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'  
    success_url = reverse_lazy('book-list') 