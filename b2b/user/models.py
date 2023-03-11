"""Models for the core app."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model for this project."""

    email = models.EmailField(_("email address"), blank=False, null=False, unique=True)

    REQUIRED_FIELDS = [
        "email",
    ]

    def __str__(self):
        """Return username."""
        return self.username
