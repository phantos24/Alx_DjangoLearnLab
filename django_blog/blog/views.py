from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login as auth_login
from django.contrib import messages
from .forms import CustomUserCreationForm,UserProfileForm, PostForm
from django.views.generic import ListView,DeleteView,CreateView,UpdateView,DetailView
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse

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

class ListView(ListView):
    model = Post
    template_name = 'blog/post_list.html' # The HTML template to use
    context_object_name = 'posts'  # The variable that holds the context data in the template
    paginate_by = 10  # Number of posts per page

class DetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html' # The HTML template to use
    context_object_name = 'posts' 

class CreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html' # The HTML template to use
    fields = ['title', 'content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(user=self.request.user)  # Pass the user to the form
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

class UpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_edit.html' # The HTML template to use
    fields = ['title', 'content']
    form_calss = PostForm

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def test_func(self):
        # Check if the logged-in user is the author of the post
        post = self.get_object()
        return self.request.user == post.author

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})
    
class DeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html' # The HTML template to use
    fields = ['title', 'content']
    success_url = '/blog/'  # Redirect to the list of posts after deletion
    
    def test_func(self):
        # Check if the logged-in user is the author of the post
        post = self.get_object()
        return self.request.user == post.author
    
def Blog(request):
    return render(request, "blog/base.html")
