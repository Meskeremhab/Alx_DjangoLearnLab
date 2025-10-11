from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    filterset_fields = ['author']  # /?author=<id>

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    filterset_fields = ['post', 'author']  # /?post=<id>

    def perform_create(self, serializer):
        # Optional: ensure you can only comment on visible posts; basic version:
        serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        # IDs of users I follow + myself
        following_ids = list(self.request.user.following.values_list('id', flat=True))
        following_ids.append(self.request.user.id)

        return Post.objects.filter(author__in=following_ids).order_by('-created_at')
