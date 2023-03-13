"""Fixtures common to the feedback app tests."""
import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from feedback.models import CLIENT_REP_GROUP, SALES_MANAGER_GROUP, MonthlyFeedback
from model_bakery import baker

from .test_feedback_api import QUESTIONNAIRES_URL


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
def questionnaire_detail_url():
    """Return a questionnaire detail url."""

    def _get_url(questionnaire_id):
        return reverse("feedback:questionnaire-detail", args=[questionnaire_id])

    return _get_url


@pytest.fixture
def response_list_url():
    """Return a questionnaire's response list url."""

    def _get_url(questionnaire_id):
        return reverse("feedback:questionnaire-responses-list", args=[questionnaire_id])

    return _get_url


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
                "choices": [
                    {"value": "True", "order": 1},
                    {"value": "False", "order": 2},
                ],
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


@pytest.fixture
def response_payload(api_client, sales_manager, questionnaire_payload):
    """Return a sample response payload."""
    # Create a questionnaire
    api_client.force_authenticate(user=sales_manager)
    response = api_client.post(QUESTIONNAIRES_URL, questionnaire_payload, format="json")

    data = response.data
    questions = data["questions"]
    question1 = questions[0]
    question2 = questions[1]
    question3 = questions[2]
    question4 = questions[3]

    choice21 = question2["choices"][0]["id"]  # id of question2 choice 1
    choice31 = question3["choices"][0]["id"]  # id of question3 choice 1
    choice32 = question3["choices"][1]["id"]  # id of question3 choice 2
    choice43 = question4["choices"][2]["id"]  # id of question4 choice 3

    return {
        "questionnaire": data["id"],
        "answers": [
            {
                "question_id": question1["id"],
                "answer_text": "My name is Solomon Botchway.",
                "choices": [],
            },
            {
                "question_id": question2["id"],
                "answer_text": "",
                "choices": [
                    {"question_choice_id": choice21},
                ],
            },
            {
                "question_id": question3["id"],
                "answer_text": "",
                "choices": [
                    {"question_choice_id": choice31},
                    {"question_choice_id": choice32},
                ],
            },
            {
                "question_id": question4["id"],
                "answer_text": "",
                "choices": [
                    {"question_choice_id": choice43},
                ],
            },
        ],
    }


@pytest.fixture
def monthly_feedback(client_rep):
    """Return a monthly feedback assigned to client_rep."""
    return baker.make(MonthlyFeedback, client_rep=client_rep)
