"""Account app models."""
from typing import List

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and return a user."""
        if not email:
            raise ValueError("Users require an email field")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Set defaults and call _create_user."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model."""

    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=100)
    email = models.EmailField(_("email address"), unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    def __str__(self):
        """Return the user's name."""
        return self.name
