"""Account app views."""
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import UserTokenSerializer

User = get_user_model()


class CreateUserTokenView(ObtainAuthToken):
    """Get token for valid user email and password."""

    serializer_class = UserTokenSerializer

    # To get the browsable API;
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
