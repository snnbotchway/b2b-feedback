"""Global project fixtures."""
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Return API client."""
    return APIClient()
