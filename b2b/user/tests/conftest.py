"""Common pytest fixtures for the user app."""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker

JWT_CREATE_URL = reverse("user:jwt-create")
User = get_user_model()


@pytest.fixture
def sample_payload():
    """Return sample user information as a payload."""
    return {
        "username": "sample_username",
        "email": "user@example.com",
        "password": "test_pass_123",
        "first_name": "First name",
        "last_name": "Last name",
    }


@pytest.fixture
def create_jwt(sample_user, api_client):
    """Create and return token pair for sample_user."""
    payload = {
        "username": sample_user.username,
        "password": "some password",
    }

    response = api_client.post(JWT_CREATE_URL, payload)

    access = response.data.get("access", None)
    refresh = response.data.get("refresh", None)
    return access, refresh, response.status_code


@pytest.fixture
def sample_user():
    """Create and return a sample user."""
    return User.objects.create_user(
        username="some_user_name",
        email="someemail@example.com",
        password="some password",
        first_name="first name",
        last_name="last name",
    )


@pytest.fixture
def inactive_user():
    """Create and return an inactive user."""
    return baker.make(User, is_active=False)


@pytest.fixture
def user_payload():
    """Return a payload of sample user information."""
    return {
        "username": "sample_user_name",
        "email": "user@example.com",
        "password": "test_pass123",
        "re_password": "test_pass123",
    }
