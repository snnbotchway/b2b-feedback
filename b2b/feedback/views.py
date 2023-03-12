"""Views for the feedback app."""
from rest_framework import mixins, viewsets

from .models import Client
from .permissions import IsSalesManager
from .serializers import ClientSerializer


class ClientViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """The Client view set."""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsSalesManager]

    def get_queryset(self):
        """Return queryset of only clients the current user is a sales manager of."""
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        return self.queryset.filter(sales_manager=user)

    def perform_create(self, serializer):
        """Assign current user as the manager on client creation."""
        return serializer.save(sales_manager=self.request.user)
