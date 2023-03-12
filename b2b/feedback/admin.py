"""Account app admin configurations."""
from django.contrib import admin
from nested_admin.nested import NestedModelAdmin, NestedStackedInline

from .models import Client, Question, QuestionChoice, Questionnaire


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Define admin configuration for the Client model."""

    autocomplete_fields = ["client_rep", "sales_manager"]
    list_display = ["email", "name", "client_rep", "sales_manager", "id"]
    list_editable = ["name"]
    list_select_related = ["client_rep", "sales_manager"]
    search_fields = ["email__icontains", "name__icontains"]


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

    autocomplete_fields = ["client_rep"]
    inlines = [QuestionInline]
    list_display = ["title", "client_rep", "created_at", "due_at", "id"]
    list_editable = ["due_at"]
    list_select_related = ["client_rep"]
    search_fields = ["title__icontains", "description__icontains"]
