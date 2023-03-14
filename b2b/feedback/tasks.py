"""Celery tasks for the feedback app."""
from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from feedback.models import Client, Questionnaire, Response

from .email import QuestionnaireReminderEmail


@shared_task
def send_reminder_emails():
    """Send reminder to questionnaires that are due in 3 days."""
    three_days_from_now = timezone.now() + timedelta(days=3)
    due_questionnaires = Questionnaire.objects.filter(
        is_active=True,
        due_at__lte=three_days_from_now,
    )

    for questionnaire in due_questionnaires:
        responded = Response.objects.filter(questionnaire=questionnaire).exists()
        if not responded:
            client_rep = questionnaire.client_rep
            clients = Client.objects.filter(client_rep=client_rep)
            client_emails = [client.email for client in clients]

            message = QuestionnaireReminderEmail(
                questionnaire_title=questionnaire.title,
            )
            message.send(client_emails)
