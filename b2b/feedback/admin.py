"""Account app admin configurations."""
from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Define admin configuration for the Client model."""

    autocomplete_fields = [
        "client_rep",
        "sales_manager",
    ]
    list_display = [
        "email",
        "name",
        "client_rep",
        "sales_manager",
        "id",
    ]
    list_editable = [
        "name",
    ]
    list_select_related = [
        "client_rep",
        "sales_manager",
    ]
    search_fields = [
        "email__icontains",
        "name__icontains",
    ]
