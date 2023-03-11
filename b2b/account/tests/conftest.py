"""Common fixtures for the account app tests."""
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_payload():
    """Return sample user information as a payload."""
    return {
        "email": "user@example.com",
        "password": "test_pass123",
        "name": "Test User",
    }


@pytest.fixture
def sample_user(user_payload):
    """Create and return a sample user."""
    return User.objects.create_user(**user_payload)
