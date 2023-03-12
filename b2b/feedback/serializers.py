"""Serializers for the feedback app."""
from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """The client serializer."""

    class Meta:
        """Client serializer meta class."""

        model = Client
        fields = [
            "id",
            "email",
            "name",
            "client_rep",
            "sales_manager",
            "created_at",
            "updated_at",
        ]
