"""User app configuration."""
from django.apps import AppConfig


class UserConfig(AppConfig):
    """User app configuration class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "user"
