from django.contrib import admin
from django.urls import path
from blog import views
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,CommentUpdateView,CommentDeleteView

urlpatterns = [
    path("", views.Blog, name="home"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_id>/comments/new/', PostDetailView.as_view(), name='comment-create'),
    path('post/<int:post_id>/comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-edit'),
    path('post/<int:post_id>/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
