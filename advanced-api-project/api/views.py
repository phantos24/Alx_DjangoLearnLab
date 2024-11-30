from django.forms import BaseModelForm
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class ListView(ListView, generics.ListAPIView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['title', 'publication_year']
    search_fields = ['title', 'author']
    ordering = ['title']

    def get_queryset(self):
        username = self.kwargs['username']
        return Book.objects.filter(purchaser__username=username)

class DetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

class CreateView(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'publication_year']  
    template_name = 'book_form.html'  
    success_url = reverse_lazy('book-list')
    permission_required = 'api.add_book'
    permission_classes = [IsAuthenticated]

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
    
    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)


class UpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'publication_year']  
    template_name = 'book_form.html'  
    success_url = reverse_lazy('book-list')
    permission_required = 'api.change_book'
    permission_classes = [IsAuthenticated]

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
    
    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)


class DeleteView(DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'  
    success_url = reverse_lazy('book-list') 