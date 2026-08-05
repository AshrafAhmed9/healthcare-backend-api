# This file defines the User table: who can log in, and how new users get created.
# Django ships with a built-in User model, but its default login field is a
# "username". This assignment logs in with email instead, so a custom User
# model is required here.

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Knows how to create a User correctly (hashes the password, etc.)."""

    use_in_migrations = True

    def create_user(self, email: str, name: str, password: str | None = None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)  # never store the raw password, only a hash of it
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, name: str, password: str | None = None, **extra_fields):
        """Used for creating an admin account from the command line."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """One row per person who has an account."""

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # can access the Django admin site
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"  # log in with email, not a username
    REQUIRED_FIELDS = ["name"]

    class Meta:
        ordering = ["-created_at"]  # newest users first

    def __str__(self) -> str:
        return self.email
