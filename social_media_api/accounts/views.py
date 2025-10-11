from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import (
    RegisterSerializer, LoginSerializer, UserPublicSerializer
)

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        user = User.objects.get(id=resp.data['id'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'user': UserPublicSerializer(user).data},
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserPublicSerializer(user).data})

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserPublicSerializer

    def get_object(self):
        return self.request.user
