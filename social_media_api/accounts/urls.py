from django.contrib import admin
from django.urls import path
from .views import UserRegistrationView, UserloginView, ProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserloginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/', ProfileView.as_view(), name='user-profile'),
]
