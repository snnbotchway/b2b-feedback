"""Fixtures common to the feedback app tests."""
import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from model_bakery import baker


@pytest.fixture
def client_payload():
    """Return sample payload of client information."""
    return {
        "email": "user@example.com",
        "name": "Test User",
    }


@pytest.fixture
def sales_manager(sample_user):
    """Return a sales manager user."""
    sales_managers = baker.make(Group, name="Sales Managers")
    sample_user.groups.add(sales_managers)
    return sample_user


@pytest.fixture
def client_detail_url():
    """Return a client detail url."""

    def _client_detail_url(client_id):
        return reverse("feedback:client-detail", args=[client_id])

    return _client_detail_url
