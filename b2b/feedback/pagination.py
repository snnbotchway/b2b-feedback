"""Feedback app pagination."""
from rest_framework.pagination import PageNumberPagination


class _PageNumberPagination10(PageNumberPagination):
    page_size = 10


class ClientPagination(PageNumberPagination):
    """Client pagination class."""

    page_size = 20


class QuestionnairePagination(_PageNumberPagination10):
    """Questionnaire pagination class."""

    pass


class ResponsePagination(PageNumberPagination):
    """Response pagination class."""

    page_size = 1


class MonthlyFeedbackPagination(_PageNumberPagination10):
    """Monthly feedback pagination."""

    pass
