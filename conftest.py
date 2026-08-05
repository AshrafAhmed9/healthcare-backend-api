# Shared setup for every test file in the project (pytest loads this
# automatically). These "fixtures" are reusable building blocks - instead of
# each test creating its own fake users and login clients, they just ask
# for one of these by name.

import pytest
from rest_framework.test import APIClient

from accounts.models import User


@pytest.fixture
def api_client() -> APIClient:
    """A test client that isn't logged in, for checking "no token" behavior."""
    return APIClient()


@pytest.fixture
def user(db) -> User:
    """The main test user - most tests act as this person."""
    return User.objects.create_user(email="alice@test.com", name="Alice", password="StrongPass123!")


@pytest.fixture
def other_user(db) -> User:
    """A second, unrelated user - used to prove one user can't see another's data."""
    return User.objects.create_user(email="bob@test.com", name="Bob", password="StrongPass123!")


@pytest.fixture
def auth_client(api_client: APIClient, user: User) -> APIClient:
    """A client that's already logged in as the main test user."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def other_auth_client(api_client: APIClient, other_user: User) -> APIClient:
    """A client that's logged in as the second, unrelated user."""
    client = APIClient()
    client.force_authenticate(user=other_user)
    return client
