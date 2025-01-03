from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login as auth_login
from django.contrib import messages
from .forms import CustomUserCreationForm,UserProfileForm, PostForm, CommentForm
from django.views.generic import ListView,DeleteView,CreateView,UpdateView,DetailView
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Q


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

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html' # The HTML template to use
    context_object_name = 'post'  # The variable that holds the context data in the template
    paginate_by = 10  # Number of posts per page

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html' # The HTML template to use
    context_object_name = 'post' 

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post)  # Fetch all comments related to this post
        return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

class PostCreateView(LoginRequiredMixin, CreateView):
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

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
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

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect('post-detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.id})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.id})

def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(title__icontains=query) |  # Case-insensitive search in title
        Q(content__icontains=query) |  # Case-insensitive search in content
        Q(tags__name__icontains=query)  # Case-insensitive search in tags)
    ).distinct()

    return render(request, 'blog/search_results.html', {'query': query, 'posts': posts})

class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Adjust to your template name
    context_object_name = 'posts'
    
    def get_queryset(self):
        tag = self.kwargs.get('tag')
        return Post.objects.filter(tags__name=tag)  # Filter posts by the tag