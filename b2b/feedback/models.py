"""Feedback app models."""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

CLIENT_REP_GROUP = "Corporate Client Representatives"
SALES_MANAGER_GROUP = "Sales Managers"


class Client(models.Model):
    """The client model."""

    email = models.EmailField()
    name = models.CharField(max_length=255)
    client_rep = models.ForeignKey(
        User,
        blank=True,
        null=True,
        limit_choices_to={"groups__name": CLIENT_REP_GROUP},
        related_name="client_rep_clients",
        on_delete=models.SET_NULL,
    )
    sales_manager = models.ForeignKey(
        User,
        blank=True,
        null=True,
        limit_choices_to={"groups__name": SALES_MANAGER_GROUP},
        related_name="sales_manager_clients",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the name."""
        return self.name


class Questionnaire(models.Model):
    """The Questionnaire model."""

    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        limit_choices_to={"groups__name": SALES_MANAGER_GROUP},
        related_name="sales_manager_questionnaires",
        on_delete=models.SET_NULL,
    )
    client_rep = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="client_rep_questionnaires",
        blank=True,
        null=True,
        limit_choices_to={"groups__name": CLIENT_REP_GROUP},
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    due_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the title."""
        return self.title


class Question(models.Model):
    """The Question model."""

    QUESTION_TYPES = [
        ("OPEN", "Open"),
        ("LOGICAL", "Logical"),
        ("MULTIPLE_CHOICE", "Multiple Choice"),
        ("DROPDOWN", "Dropdown"),
    ]
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, related_name="questions"
    )
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPES)
    question_text = models.TextField()
    required = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        """Return the question_text."""
        return self.question_text


class QuestionChoice(models.Model):
    """The QuestionChoice model."""

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    value = models.TextField()
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        """Return the value."""
        return self.value


class Response(models.Model):
    """The Response model."""

    respondent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="client_rep_responses",
        limit_choices_to={"groups__name": CLIENT_REP_GROUP},
        null=True,
    )
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, related_name="questionnaire_responses"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return response summary."""
        return f"{self.respondent}'s response to {self.questionnaire}"


class Answer(models.Model):
    """The Answer model."""

    response = models.ForeignKey(
        Response, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(null=True, blank=True)

    def __str__(self):
        """Return the answer_text."""
        return f"Answer to {self.question}"


class AnswerChoice(models.Model):
    """The Answer Choice model."""

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="choices")
    question_choice = models.ForeignKey(
        QuestionChoice, on_delete=models.CASCADE, related_name="answer_choices"
    )

    def __str__(self):
        """Return the question_choice value."""
        return str(self.question_choice)
