import pytest
from rest_framework.test import APIClient

from accounts.models import User


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(email="alice@test.com", name="Alice", password="StrongPass123!")


@pytest.fixture
def other_user(db) -> User:
    return User.objects.create_user(email="bob@test.com", name="Bob", password="StrongPass123!")


@pytest.fixture
def auth_client(api_client: APIClient, user: User) -> APIClient:
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def other_auth_client(api_client: APIClient, other_user: User) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=other_user)
    return client
