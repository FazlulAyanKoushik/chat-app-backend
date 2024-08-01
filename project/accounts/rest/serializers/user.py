"""Serializers for user model."""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "first_name", "last_name"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Login serializer."""
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            msg = "Unable to log in with provided credentials."
            raise serializers.ValidationError(msg, code="authorization")

        if not user.is_active:
            msg = "User account is disabled."
            raise serializers.ValidationError(msg, code="authorization")

        return {
            "email": user.email,
            "id": user.id,
        }
