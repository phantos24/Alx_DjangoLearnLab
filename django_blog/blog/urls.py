from django.contrib import admin
from django.urls import path
from blog import views
from .views import ListView,DetailView,CreateView,UpdateView,DeleteView

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path('posts/', ListView.as_view(), name='listview'),
    path('posts/<int:pk>/', DetailView.as_view(), name='detailview'),
    path('posts/new/', CreateView.as_view(), name='createview'),
    path('posts/<int:pk>/edit/', UpdateView.as_view(), name='updateview'),
    path('posts/<int:pk>/delete/', DeleteView.as_view(), name='deleteview'),
]
