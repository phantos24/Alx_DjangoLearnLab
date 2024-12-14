from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.views import APIView
from.serializers import UserRegistrationSerializer, UserLoginSerializer,TokenSerializer, UserProfileSerializer
from django.urls import reverse_lazy
from .forms import UserCreationForm, UserLoginForm
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .models import User


# Create your views here.

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]   
    def get(self, request):
        form_class = UserCreationForm
        return render(request, 'accounts/register.html', {'form': form_class()})


    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if  serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserloginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        form_class = UserLoginForm
        return render(request, 'accounts/login.html', {'form': form_class()})
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                redirect('profile')
            else:
                return render(request, 'accounts/login.html', {"error": "Invalid credentials"})
        return render(request, 'accounts/login.html', {"errors": serializer.errors})
    
class TokenRetrieveView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Retrieve or create a token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, username=None, format=None):
        try:
            if username:
                user = User.objects.get(username=username)
            else:
                user = request.user

            if format == 'html':
                return render(request, 'accounts/profile.html', {'user': user})
            else:
                serializer = UserProfileSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)