import pytest
from rest_framework import status

from accounts.models import User

pytestmark = pytest.mark.django_db


def test_register_creates_user_and_returns_tokens(api_client):
    response = api_client.post(
        "/api/auth/register/",
        {"email": "new@test.com", "name": "New User", "password": "StrongPass123!"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["user"]["email"] == "new@test.com"
    assert "access" in response.data and "refresh" in response.data
    assert User.objects.filter(email="new@test.com").exists()


def test_register_rejects_weak_password(api_client):
    response = api_client.post(
        "/api/auth/register/",
        {"email": "weak@test.com", "name": "Weak", "password": "123"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_rejects_duplicate_email(api_client, user):
    response = api_client.post(
        "/api/auth/register/",
        {"email": user.email, "name": "Someone Else", "password": "StrongPass123!"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_with_valid_credentials(api_client, user):
    response = api_client.post(
        "/api/auth/login/", {"email": user.email, "password": "StrongPass123!"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert response.data["user"]["email"] == user.email


def test_login_with_invalid_credentials(api_client, user):
    response = api_client.post(
        "/api/auth/login/", {"email": user.email, "password": "wrong-password"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_me_requires_authentication(api_client):
    response = api_client.get("/api/auth/me/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_me_returns_current_user(auth_client, user):
    response = auth_client.get("/api/auth/me/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email
