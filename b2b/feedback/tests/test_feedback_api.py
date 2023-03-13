import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from feedback.models import (
    CLIENT_REP_GROUP,
    AnswerChoice,
    Client,
    Questionnaire,
    Response,
)
from feedback.serializers import (
    ClientSerializer,
    QuestionnaireSerializer,
    ResponseSerializer,
)
from model_bakery import baker
from rest_framework import status

User = get_user_model()

CLIENTS_URL = reverse("feedback:client-list")
QUESTIONNAIRES_URL = reverse("feedback:questionnaire-list")


@pytest.mark.django_db
class TestManageClients:
    """Test the sales manager manage client endpoints."""

    def test_sales_manager_create_client_returns_201(
        self, api_client, client_payload, sales_manager
    ):
        """Test sales manager can create client."""
        api_client.force_authenticate(user=sales_manager)

        response = api_client.post(CLIENTS_URL, client_payload)

        client = Client.objects.get(pk=response.data.get("id"))
        serializer = ClientSerializer(client)
        assert response.data == serializer.data
        assert response.status_code == status.HTTP_201_CREATED
        assert Client.objects.count() == 1

    def test_non_sales_manager_create_client_returns_403(
        self, api_client, client_payload, sample_user
    ):
        """Test only sales managers can create clients."""
        api_client.force_authenticate(user=sample_user)

        response = api_client.post(CLIENTS_URL, client_payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Client.objects.count() == 0

    def test_sales_manager_list_clients_returns_200(self, api_client, sales_manager):
        """Test sales manager can list clients."""
        api_client.force_authenticate(user=sales_manager)
        baker.make(Client)
        baker.make(Client, sales_manager=sales_manager)

        response = api_client.get(CLIENTS_URL)

        clients = Client.objects.filter(sales_manager=sales_manager)
        serializer = ClientSerializer(clients, many=True)
        assert response.data == serializer.data
        assert len(response.data) == 1
        assert response.status_code == status.HTTP_200_OK
        assert Client.objects.count() == 2

    def test_non_sales_manager_list_client_returns_403(self, api_client, sample_user):
        """Test only sales managers can list clients."""
        api_client.force_authenticate(user=sample_user)

        response = api_client.get(CLIENTS_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_sales_manager_delete_client_returns_204(
        self, api_client, client_detail_url, sales_manager
    ):
        """Test sales manager can delete only his clients."""
        api_client.force_authenticate(user=sales_manager)
        client = baker.make(Client, sales_manager=sales_manager)
        other_client = baker.make(Client)
        url = client_detail_url(client.id)

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Client.objects.count() == 1

        url = client_detail_url(other_client.id)

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Client.objects.count() == 1

    def test_non_sales_manager_delete_client_returns_403(
        self, api_client, client_detail_url, sample_user
    ):
        """Test only sales managers can delete clients."""
        api_client.force_authenticate(user=sample_user)
        client = baker.make(Client)
        url = client_detail_url(client.id)

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Client.objects.count() == 1


@pytest.mark.django_db
class TestManageQuestionnaires:
    """Tests on questionnaire management."""

    def test_create_questionnaire_returns_201(
        self, api_client, questionnaire_payload, sales_manager
    ):
        """Test creating a questionnaire is successful."""
        api_client.force_authenticate(user=sales_manager)

        response = api_client.post(
            QUESTIONNAIRES_URL, questionnaire_payload, format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        questionnaires = Questionnaire.objects.filter(
            client_rep_id=response.data.get("client_rep")
        )
        assert questionnaires.count() == 1
        questionnaire = questionnaires.first()
        assert questionnaire.questions.count() == 4
        serializer = QuestionnaireSerializer(questionnaire)
        assert response.data == serializer.data

        # Assert that the last two questions are not required just like in the payload
        questions = questionnaire.questions.all()
        assert questions[0].required == questions[1].required is True
        assert questions[2].required == questions[3].required is False

    def test_only_sales_manager_can_create_questionnaire(
        self, api_client, questionnaire_payload, sample_user
    ):
        """Test non sales manager cannot create a questionnaire."""
        api_client.force_authenticate(user=sample_user)

        response = api_client.post(
            QUESTIONNAIRES_URL, questionnaire_payload, format="json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Questionnaire.objects.count() == 0

    def test_client_rep_can_list_assigned_questionnaires(self, api_client, client_rep):
        """Test client reps can list their questionnaires."""
        api_client.force_authenticate(user=client_rep)
        baker.make(Questionnaire, client_rep=client_rep)
        baker.make(Questionnaire)

        response = api_client.get(QUESTIONNAIRES_URL)

        assert response.status_code == status.HTTP_200_OK
        questionnaires = Questionnaire.objects.filter(client_rep=client_rep)
        serializer = QuestionnaireSerializer(questionnaires, many=True)
        assert serializer.data == response.data
        assert len(response.data) == 1

    def test_non_client_rep_cannot_list_questionnaires(self, api_client, sample_user):
        """Test non client reps cannot list questionnaires."""
        api_client.force_authenticate(user=sample_user)
        baker.make(Questionnaire, client_rep=sample_user)
        baker.make(Questionnaire)

        response = api_client.get(QUESTIONNAIRES_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        questionnaires = Questionnaire.objects.filter(client_rep=sample_user)
        serializer = QuestionnaireSerializer(questionnaires, many=True)
        assert serializer.data != response.data


@pytest.mark.django_db
class TestManageResponses:
    """Tests on questionnaire management."""

    def test_client_rep_create_response_returns_201(
        self, api_client, client_rep, response_list_url, response_payload
    ):
        """Test creating a questionnaire is successful."""
        api_client.force_authenticate(user=client_rep)
        questionnaire = Questionnaire.objects.get(client_rep=client_rep)
        url = response_list_url(questionnaire.id)

        response = api_client.post(url, response_payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        responses = Response.objects.filter(respondent=response.data["respondent"])
        assert responses.count() == 1
        feedback_response = responses.first()
        assert feedback_response.questionnaire == questionnaire
        assert feedback_response.respondent == client_rep
        assert feedback_response.answers.count() == 4
        assert AnswerChoice.objects.count() == 4
        serializer = ResponseSerializer(feedback_response)
        assert response.data == serializer.data

    def test_client_reps_cannot_respond_unassigned_questionnaires(
        self, api_client, client_rep, response_list_url, response_payload
    ):
        """Test client reps can't respond if they haven't been assigned."""
        user = baker.make(User)
        client_reps = Group.objects.get(name=CLIENT_REP_GROUP)
        user.groups.add(client_reps)
        api_client.force_authenticate(user=user)
        questionnaire = Questionnaire.objects.get(client_rep=client_rep)
        url = response_list_url(questionnaire.id)

        response = api_client.post(url, response_payload, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Response.objects.count() == 0

    def test_anonymous_user_cannot_respond_to_questionnaires(
        self, api_client, response_list_url, response_payload
    ):
        """Test anonymous users cannot respond to questionnaires."""
        api_client.logout()
        questionnaire = baker.make(Questionnaire)
        url = response_list_url(questionnaire.id)

        response = api_client.post(url, response_payload, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Response.objects.count() == 0
