"""Fixtures common to the feedback app tests."""
import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from feedback.models import CLIENT_REP_GROUP, SALES_MANAGER_GROUP
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
    sales_managers = baker.make(Group, name=SALES_MANAGER_GROUP)
    sample_user.groups.add(sales_managers)
    return sample_user


@pytest.fixture
def client_rep(sample_user):
    """Return a client representative user."""
    client_reps = baker.make(Group, name=CLIENT_REP_GROUP)
    sample_user.groups.add(client_reps)
    return sample_user


@pytest.fixture
def client_detail_url():
    """Return a client detail url."""

    def _client_detail_url(client_id):
        return reverse("feedback:client-detail", args=[client_id])

    return _client_detail_url


@pytest.fixture
def questionnaire_payload(client_rep):
    """Return a sample questionnaire."""
    return {
        "client_rep": client_rep.id,
        "title": "Sample title",
        "description": "Sample description",
        "due_at": "2022-07-12T18:30:45Z",
        "questions": [
            {
                "question_type": "OPEN",
                "question_text": "What is your name?",
                "required": True,
                "order": 1,
                "choices": [],
            },
            {
                "question_type": "LOGICAL",
                "question_text": "True or False?",
                "required": True,
                "order": 2,
                "choices": [],
            },
            {
                "question_type": "MULTIPLE_CHOICE",
                "question_text": "Select all which apply.",
                "required": False,
                "order": 3,
                "choices": [
                    {"value": "Option 1", "order": 1},
                    {"value": "Option 2", "order": 2},
                    {"value": "Option 3", "order": 3},
                ],
            },
            {
                "question_type": "DROPDOWN",
                "question_text": "Which of the following?",
                "order": 4,
                "choices": [
                    {"value": "Option 1", "order": 1},
                    {"value": "Option 2", "order": 2},
                    {"value": "Option 3", "order": 3},
                ],
            },
        ],
    }
