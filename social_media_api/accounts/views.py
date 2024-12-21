from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status, generics
from rest_framework.views import APIView
from.serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer
from django.urls import reverse_lazy
from .forms import UserCreationForm, UserLoginForm
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from .models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token



# Create your views here.

CustomUser = get_user_model()

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
                return redirect('profile')
                #return Response({'token': token.key, 'redirect_url': reverse_lazy('profile')}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
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
    
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # Retrieve all users to demonstrate the use of CustomUser.objects.all()
        users = CustomUser.objects.all()
        user_to_follow = get_object_or_404(users, id=user_id)
        
        if user_to_follow == request.user:
            return Response({'error': 'You cannot follow yourself.'}, status=400)
        
        request.user.following.add(user_to_follow)
        return Response({'message': f'Successfully followed {user_to_follow.username}.'})

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # Retrieve all users to demonstrate the use of CustomUser.objects.all()
        users = CustomUser.objects.all()
        user_to_unfollow = get_object_or_404(users, id=user_id)
        
        if user_to_unfollow == request.user:
            return Response({'error': 'You cannot unfollow yourself.'}, status=400)
        
        request.user.following.remove(user_to_unfollow)
        return Response({'message': f'Successfully unfollowed {user_to_unfollow.username}.'})
