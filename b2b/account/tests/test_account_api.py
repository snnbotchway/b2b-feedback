import pytest
from django.urls import reverse
from rest_framework import status

ACCOUNT_LOGIN_URL = reverse("account:login")


@pytest.mark.django_db
class TestUserToken:
    def test_generate_token_with_valid_credentials_returns_200(
        self, sample_user, api_client
    ):
        """Test a token is returned with valid credentials"""
        payload = {
            "email": sample_user.email,
            "password": "test_pass123",
        }

        response = api_client.post(ACCOUNT_LOGIN_URL, payload)

        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.data

    def test_generate_token_with_invalid_email_returns_400(
        self, sample_user, api_client
    ):
        """Test a token is not returned with invalid email"""
        payload = {
            "email": "other@example.com",
            "password": "testPass123",
        }

        response = api_client.post(ACCOUNT_LOGIN_URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "token" not in response.data

    def test_generate_token_with_invalid_password_returns_400(
        self, sample_user, api_client
    ):
        """Test a token is not returned with invalid password"""
        payload = {
            "email": sample_user.email,
            "password": "badPass123",
        }

        response = api_client.post(ACCOUNT_LOGIN_URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "token" not in response.data

    def test_generate_token_without_password_returns_400(self, api_client, sample_user):
        """Test a token is not returned with blank password"""
        payload = {
            "email": "user@example.com",
            "password": "",
        }

        response = api_client.post(ACCOUNT_LOGIN_URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "token" not in response.data
