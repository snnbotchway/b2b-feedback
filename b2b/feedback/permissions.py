"""Custom permissions for the feedback app."""
from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission

from .models import SALES_MANAGER_GROUP


class IsSalesManager(BasePermission):
    """Permission class to check if a user is in the Sales Managers group."""

    def has_permission(self, request, view):
        """Return true if current user is in the Sales Mangers group."""
        sales_manager_group = Group.objects.get_or_create(name=SALES_MANAGER_GROUP)
        return sales_manager_group in request.user.groups.all()
