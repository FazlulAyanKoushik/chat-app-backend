"""Views for user management."""

from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from accounts.TokenAuthentications import JWTAuthentication
from accounts.rest.serializers.user import UserSerializer, LoginSerializer

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    """List and create users."""

    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    """List users."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()


class LoginView(generics.GenericAPIView):
    """Login view."""

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = JWTAuthentication.generate_token(serializer.validated_data)
            return Response({
                "message": "Login successful",
                "token": token,
                "user": serializer.validated_data,
            }, status=200)
        return Response(serializer.errors, status=400)
