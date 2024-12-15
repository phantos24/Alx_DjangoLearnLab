from django.urls import path, include
from .views import PostView, CommentView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'posts', PostView)
router.register(r'comments', CommentView)

urlpatterns = [
    path('', include(router.urls)),
]