# Serializers convert between a User row in the database and the JSON
# a client sends/receives over the API. This file has three of them,
# one for each situation where user data needs to move in or out.

from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """Read-only view of a user. Used to show "who am I" without exposing the password."""

    class Meta:
        model = User
        fields = ["id", "email", "name", "created_at"]
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """Handles new sign-ups: takes email/name/password, creates the account."""

    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["id", "email", "name", "password"]
        read_only_fields = ["id"]

    def validate_password(self, value: str) -> str:
        # Rejects weak passwords (too short, too common, etc.) before saving.
        password_validation.validate_password(value)
        return value

    def create(self, validated_data: dict) -> User:
        # create_user() hashes the password properly instead of storing it as plain text.
        return User.objects.create_user(**validated_data)


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Handles login: checks email + password, returns a login token if correct."""

    username_field = User.USERNAME_FIELD  # log in with email instead of a username

    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs)  # does the actual password check, builds the token
        data["user"] = UserSerializer(self.user).data  # also send back who just logged in
        return data
