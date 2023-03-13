"""Feedback app validators."""
import re

from django.core.exceptions import ValidationError


def validate_month_format(value):
    """Validate the YYYY-MM month format."""
    pattern = r"^\d{4}-\d{2}$"
    if not re.match(pattern, value):
        raise ValidationError("Month format should be YYYY-MM")
