"""The feedback app configuration."""
from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    """The feedback app configuration class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "feedback"
