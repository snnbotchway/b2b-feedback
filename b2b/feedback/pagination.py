"""Feedback app pagination."""
from rest_framework.pagination import PageNumberPagination


class ResponsePagination(PageNumberPagination):
    """Response pagination class."""

    page_size = 1
