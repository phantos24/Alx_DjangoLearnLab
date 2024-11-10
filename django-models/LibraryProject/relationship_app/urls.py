from django.urls import path
from .import views

urlpatterns = [
    path('books/', views.book_list, name='books'),
    path('library/', views.LibraryView.as_view(), name='library'),
]