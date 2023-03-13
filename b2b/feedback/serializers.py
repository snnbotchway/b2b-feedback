"""Serializers for the feedback app."""
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import (
    Answer,
    AnswerChoice,
    Client,
    Question,
    QuestionChoice,
    Questionnaire,
    Response,
)


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

    class Meta:
        """Question choice serializer meta class."""

        model = QuestionChoice
        fields = [
            "id",
            "value",
            "order",
        ]


class QuestionSerializer(serializers.ModelSerializer):
    """The question serializer."""

    choices = QuestionChoiceSerializer(many=True, required=False)

    class Meta:
        """Question serializer meta class."""

        model = Question
        fields = [
            "id",
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


class AnswerChoiceSerializer(serializers.ModelSerializer):
    """The answer choice serializer."""

    question_choice_id = serializers.IntegerField()

    class Meta:
        """Answer choice serializer meta class."""

        model = AnswerChoice
        fields = [
            "id",
            "question_choice_id",
        ]


class AnswerSerializer(serializers.ModelSerializer):
    """The answer serializer."""

    choices = AnswerChoiceSerializer(many=True, required=False)
    question_id = serializers.IntegerField()

    class Meta:
        """Answer serializer meta class."""

        model = Answer
        fields = [
            "id",
            "answer_text",
            "question_id",
            "choices",
        ]


class ResponseSerializer(serializers.ModelSerializer):
    """The response serializer."""

    answers = AnswerSerializer(many=True, required=True)

    class Meta:
        """Response serializer meta class."""

        model = Response
        fields = [
            "id",
            "respondent",
            "submitted_at",
            "answers",
        ]
        read_only_fields = [
            "respondent",
        ]

    def create(self, validated_data):
        """Create a response."""
        with transaction.atomic():
            answers = validated_data.pop("answers", [])
            response = Response.objects.create(**validated_data)

            for answer in answers:
                choices = answer.pop("choices", [])
                answer = Answer.objects.create(**answer, response=response)
                choice_objs = [
                    AnswerChoice(**choice, answer=answer) for choice in choices
                ]
                AnswerChoice.objects.bulk_create(choice_objs)

            return response

    def validate(self, attrs):
        """Validate that current user is assigned to the questionnaire."""
        questionnaire = get_object_or_404(
            Questionnaire, pk=self.context["questionnaire_id"]
        )
        if questionnaire.client_rep != self.context["user"]:
            raise Http404()
        return super().validate(attrs)
