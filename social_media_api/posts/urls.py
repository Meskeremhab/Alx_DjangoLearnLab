from django.urls import path
from .views import CreatePostView, FeedView

urlpatterns = [
    path('posts/', CreatePostView.as_view(), name='create-post'),
    path('feed/',  FeedView.as_view(),      name='feed'),
]
