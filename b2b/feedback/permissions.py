"""Custom permissions for the feedback app."""
from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission

from .models import CLIENT_REP_GROUP, SALES_MANAGER_GROUP


class IsSalesManager(BasePermission):
    """Permission class to check if a user is in the Sales Managers group."""

    def has_permission(self, request, view):
        """Return true if current user is in the Sales Mangers group."""
        sales_manager_group, _ = Group.objects.get_or_create(name=SALES_MANAGER_GROUP)
        return sales_manager_group in request.user.groups.all()


class IsClientRepresentative(BasePermission):
    """Permission class to check if a user is in the Client Representatives group."""

    def has_permission(self, request, view):
        """Return true if current user is in the Client Representatives group."""
        client_rep_group, _ = Group.objects.get_or_create(name=CLIENT_REP_GROUP)
        return client_rep_group in request.user.groups.all()


class IsSalesManagerOrClientRep(BasePermission):
    """Sales Managers or Client Representatives permission class."""

    def has_permission(self, request, view):
        """Return true if current user is in either group."""
        sales_manager_group, _ = Group.objects.get_or_create(name=SALES_MANAGER_GROUP)
        client_rep_group, _ = Group.objects.get_or_create(name=CLIENT_REP_GROUP)

        user_groups = request.user.groups.all()
        return sales_manager_group in user_groups or client_rep_group in user_groups
