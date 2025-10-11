from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer

class CreatePostView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        # Posts from people I follow + my own posts
        following_ids = self.request.user.following.values_list('id', flat=True)
        return Post.objects.filter(author__in=list(following_ids) + [self.request.user.id]).order_by('-created_at')
