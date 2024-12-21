from django.urls import path, include
from .views import PostView, CommentView, FeedView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'posts', PostView)
router.register(r'comments', CommentView)

urlpatterns = [
    path('', include(router.urls)),
     path('feed/', FeedView.as_view(), name='feed'),
]