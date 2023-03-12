"""Serializers for the feedback app."""
from django.db import transaction
from rest_framework import serializers

from .models import Client, Question, QuestionChoice, Questionnaire


class ClientSerializer(serializers.ModelSerializer):
    """The client serializer."""

    class Meta:
        """Client serializer meta class."""

        model = Client
        fields = [
            "id",
            "email",
            "name",
            "client_rep",
            "sales_manager",
            "created_at",
            "updated_at",
        ]


class QuestionChoiceSerializer(serializers.ModelSerializer):
    """The question choice serializer."""

    # question = serializers.IntegerField(read_only=True)

    class Meta:
        """Question choice serializer meta class."""

        model = QuestionChoice
        fields = [
            "id",
            # "question",
            "value",
            "order",
        ]


class QuestionSerializer(serializers.ModelSerializer):
    """The question serializer."""

    choices = QuestionChoiceSerializer(many=True, required=False)
    # questionnaire = serializers.IntegerField(read_only=True)

    class Meta:
        """Question serializer meta class."""

        model = Question
        fields = [
            "id",
            # "questionnaire",
            "question_type",
            "question_text",
            "order",
            "required",
            "choices",
        ]


class QuestionnaireSerializer(serializers.ModelSerializer):
    """The questionnaire serializer."""

    questions = QuestionSerializer(many=True, required=True)

    class Meta:
        """Questionnaire serializer meta class."""

        model = Questionnaire
        fields = [
            "id",
            "client_rep",
            "title",
            "description",
            "is_active",
            "due_at",
            "created_at",
            "questions",
        ]

    def create(self, validated_data):
        """Create a questionnaire."""
        with transaction.atomic():
            questions = validated_data.pop("questions", [])
            questionnaire = Questionnaire.objects.create(**validated_data)

            for question in questions:
                choices = question.pop("choices", [])
                question = Question.objects.create(
                    **question, questionnaire=questionnaire
                )
                choice_objs = [
                    QuestionChoice(**choice, question=question) for choice in choices
                ]
                QuestionChoice.objects.bulk_create(choice_objs)

            return questionnaire

    def validate_questions(self, value):
        """Raise error if there are no questions."""
        if not value:
            raise serializers.ValidationError("At least one question is required.")
        return value
