"""Views for the feedback app."""
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Client, Questionnaire
from .permissions import IsSalesManager
from .serializers import ClientSerializer, QuestionnaireSerializer


class ClientViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
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


class QuestionnaireViewSet(
    CreateModelMixin,
    GenericViewSet,
):
    """The questionnaire viewset."""

    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    permission_classes = [IsSalesManager]
