from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login as auth_login
from django.contrib import messages
from .forms import CustomUserCreationForm,UserProfileForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Use Django's auth_login function to log in the user
            messages.success(request, 'You have successfully logged in!')
            return redirect('profile')  # Redirect to the user's profile
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, "blog/login.html")
def logout(request):
    return render(request,"blog/logout.html")

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')  # Redirect to the user's profile
        else:
            messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = CustomUserCreationForm()
    return render(request,"blog/register.html", {'form':form})

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = get_user_model()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request,'Failed to update profile. Please check the form for errors.')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': form})     