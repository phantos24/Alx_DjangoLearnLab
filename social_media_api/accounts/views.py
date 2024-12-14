from urllib import request
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.views import APIView
from.serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer
from django.urls import reverse_lazy
from .forms import UserCreationForm, UserLoginForm
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework.authtoken.models import Token



# Create your views here.

class UserRegistrationView(APIView):
    def get(self, request):
        form_class = UserCreationForm
        return render(request, 'accounts/register.html', {'form': form_class()})

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if  serializer.is_valid():
            serializer.save()
            return redirect('login')
            #return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserloginView(APIView):
    def get(self, request):
        form_class = UserLoginForm
        return render(request, 'accounts/login.html', {'form': form_class()})
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'], 
                                password=serializer.validated_data['password'])
            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                #return redirect('profile')
                return Response({'token': token.key, 'redirect_url': reverse_lazy('profile')}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)