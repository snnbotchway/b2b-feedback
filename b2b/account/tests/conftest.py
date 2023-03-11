"""Common fixtures for the account app tests."""
import pytest


@pytest.fixture
def user_payload():
    """Return sample user information as a payload."""
    return {
        "email": "user@example.com",
        "password": "test_pass123",
        "name": "Test User",
    }
