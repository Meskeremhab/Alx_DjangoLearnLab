from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    filterset_fields = ['author']  # /?author=<id>

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    filterset_fields = ['post', 'author']  # /?post=<id>

    def perform_create(self, serializer):
        # Optional: ensure you can only comment on visible posts; basic version:
        serializer.save(author=self.request.user)
