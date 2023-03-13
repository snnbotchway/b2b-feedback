"""Views for the feedback app."""
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import GenericViewSet

from .models import Client, Questionnaire, Response
from .pagination import ResponsePagination
from .permissions import (
    IsClientRepresentative,
    IsSalesManager,
    IsSalesManagerOrClientRep,
)
from .serializers import (
    ClientSerializer,
    QuestionnaireListSerializer,
    QuestionnaireSerializer,
    ResponseSerializer,
)


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
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """The questionnaire viewset."""

    queryset = Questionnaire.objects.prefetch_related("questions__choices").all()
    serializer_class = QuestionnaireSerializer

    def _fetch_params(self):
        query_params = self.request.query_params
        sales_manager = int(query_params.get("sales_manager", 0))
        client_rep = int(query_params.get("client_rep", 0))
        return client_rep, sales_manager

    def get_queryset(self):
        """Filter queryset with params."""
        user = self.request.user
        client_rep, sales_manager = self._fetch_params()
        if client_rep:
            return self.queryset.filter(client_rep=user)
        elif sales_manager:
            return self.queryset.filter(author=user)
        return self.queryset

    def get_permissions(self):
        """Return appropriate permissions."""
        if self.request.method in SAFE_METHODS:
            return [IsSalesManagerOrClientRep()]
        return [IsSalesManager()]

    def get_serializer_class(self):
        """Return appropriate serializer."""
        if self.action == "list":
            return QuestionnaireListSerializer
        return QuestionnaireSerializer

    def perform_create(self, serializer):
        """Set current user as questionnaire author."""
        return serializer.save(author=self.request.user)


class ResponseViewSet(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """The Response viewset."""

    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    pagination_class = ResponsePagination

    def get_queryset(self):
        """Filter responses with questionnaire id in url."""
        return self.queryset.filter(
            questionnaire_id=self.kwargs["questionnaire_pk"]
        ).order_by("id")

    def get_permissions(self):
        """Return appropriate permissions."""
        if self.request.method in SAFE_METHODS:
            return [IsSalesManager()]
        return [IsClientRepresentative()]

    def get_serializer_context(self):
        """Pass user and questionnaire id to serializer for validation."""
        return {
            "user": self.request.user,
            "questionnaire_id": self.kwargs["questionnaire_pk"],
        }

    def perform_create(self, serializer):
        """Add response relationships."""
        questionnaire_id = self.kwargs["questionnaire_pk"]
        return serializer.save(
            questionnaire_id=questionnaire_id, respondent=self.request.user
        )
