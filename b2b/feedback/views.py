"""Views for the feedback app."""
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Client, Questionnaire, Response
from .permissions import IsClientRepresentative, IsSalesManager
from .serializers import ClientSerializer, QuestionnaireSerializer, ResponseSerializer


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
    ListModelMixin,
    GenericViewSet,
):
    """The questionnaire viewset."""

    queryset = Questionnaire.objects.prefetch_related("questions__choices").all()
    serializer_class = QuestionnaireSerializer

    def _is_list_action(self):
        return self.action == "list"

    def get_queryset(self):
        """Filter list queryset to questionnaires the current user is assigned."""
        if self._is_list_action():
            return self.queryset.filter(client_rep=self.request.user)
        return self.queryset

    def get_permissions(self):
        """Client reps can list and Sales managers can create questionnaires."""
        if self._is_list_action():
            return [IsClientRepresentative()]
        return [IsSalesManager()]


class ResponseViewSet(
    CreateModelMixin,
    GenericViewSet,
):
    """The Response viewset."""

    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [IsClientRepresentative]

    def perform_create(self, serializer):
        """Attach current user as the respondent."""
        return serializer.save(respondent=self.request.user)
