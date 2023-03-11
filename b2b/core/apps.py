"""Core app configuration."""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Core app config class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
