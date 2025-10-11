from rest_framework import permissions, status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import FollowActionSerializer, UserPublicSerializer

User = get_user_model()

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowActionSerializer

    def post(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=400)
       
       
        request.user.following.add(target)


        return Response(
            {"detail": f"Now following {target.username}"},
            status=status.HTTP_200_OK
        )

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowActionSerializer

    def post(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=400)
        request.user.following.remove(target)
        return Response(
            {"detail": f"Unfollowed {target.username}"},
            status=status.HTTP_200_OK
        )
