from django.contrib import admin
from django.urls import path
from .views import UserRegistrationView, UserloginView, TokenRetrieveView, ProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserloginView.as_view(), name='login'),
    path('token/', TokenRetrieveView.as_view(), name='token'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/', ProfileView.as_view(), name='user-profile'),
]
