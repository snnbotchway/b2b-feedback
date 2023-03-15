"""Account app admin configurations."""
from django.contrib import admin
from nested_admin.nested import NestedModelAdmin, NestedStackedInline

from .models import (
    Answer,
    AnswerChoice,
    Client,
    MonthlyFeedback,
    Question,
    QuestionChoice,
    Questionnaire,
    Response,
)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Define admin configuration for the Client model."""

    autocomplete_fields = ["client_rep", "sales_manager"]
    list_display = ["email", "name", "client_rep", "sales_manager", "id"]
    list_editable = ["name"]
    list_select_related = ["client_rep", "sales_manager"]
    search_fields = ["email", "name"]


class QuestionChoiceInline(NestedStackedInline):
    """Inline class for question choices."""

    model = QuestionChoice
    extra = 0


class QuestionInline(NestedStackedInline):
    """Inline class for questionnaire questions."""

    model = Question
    inlines = [QuestionChoiceInline]
    extra = 0


@admin.register(Questionnaire)
class QuestionnaireAdmin(NestedModelAdmin):
    """Define admin configuration for the Questionnaire model."""

    autocomplete_fields = ["author", "client_rep"]
    inlines = [QuestionInline]
    list_display = ["title", "client_rep", "created_at", "due_at", "id"]
    list_editable = ["due_at"]
    list_select_related = ["client_rep"]
    search_fields = ["title", "client_rep__name"]


class AnswerChoiceInline(NestedStackedInline):
    """Inline class for answer choices."""

    model = AnswerChoice
    extra = 0


class AnswerInline(NestedStackedInline):
    """Inline class for response answers."""

    model = Answer
    inlines = [AnswerChoiceInline]
    extra = 0


@admin.register(Response)
class ResponseAdmin(NestedModelAdmin):
    """Define admin configuration for the Questionnaire model."""

    autocomplete_fields = ["questionnaire", "respondent"]
    inlines = [AnswerInline]
    list_select_related = ["questionnaire", "respondent"]
    search_fields = ["questionnaire__title", "respondent__email"]


@admin.register(MonthlyFeedback)
class MonthlyFeedbackAdmin(admin.ModelAdmin):
    """Define admin site configuration for monthly feedback."""

    autocomplete_fields = ["client_rep"]
    list_select_related = ["client_rep"]
    search_fields = ["month", "client_rep__name"]
