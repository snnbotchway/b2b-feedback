import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserManager:
    def test_create_user(self, user_payload):
        user = User.objects.create_user(**user_payload)
        assert user.email == user_payload.get("email")
        assert user.name == user_payload.get("name")
        assert user.check_password(user_payload.get("password"))
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_user_missing_email(self):
        with pytest.raises(ValueError) as excinfo:
            User.objects.create_user(email=None, password="password")
        assert str(excinfo.value) == "Users require an email field"

    def test_create_superuser(self):
        email = "testsuperuser@example.com"
        password = "password"
        user = User.objects.create_superuser(email=email, password=password)
        assert user.email == email
        assert user.is_staff
        assert user.is_superuser

    def test_create_superuser_missing_is_staff(self, user_payload):
        with pytest.raises(ValueError) as excinfo:
            User.objects.create_superuser(**user_payload, is_staff=False)
        assert str(excinfo.value) == "Superuser must have is_staff=True."

    def test_create_superuser_missing_is_superuser(self, user_payload):
        with pytest.raises(ValueError) as excinfo:
            User.objects.create_superuser(**user_payload, is_superuser=False)
        assert str(excinfo.value) == "Superuser must have is_superuser=True."
