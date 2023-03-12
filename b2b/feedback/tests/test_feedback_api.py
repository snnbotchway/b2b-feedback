import pytest
from django.urls import reverse
from feedback.models import Client, Questionnaire
from feedback.serializers import ClientSerializer, QuestionnaireSerializer
from model_bakery import baker
from rest_framework import status

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
class TestQuestionnaires:
    """Tests on questionnaire management."""

    def test_create_questionnaire_returns_201(
        self, api_client, client_rep, questionnaire_payload, sales_manager
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

        # Assert the last two questions are false just like in the payload
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
