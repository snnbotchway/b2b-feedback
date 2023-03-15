"""Email classes for the feedback app."""
from templated_mail.mail import BaseEmailMessage


class QuestionnaireReminderEmail(BaseEmailMessage):
    """Email for questionnaire is due reminders."""

    template_name = "email/questionnaire_reminder.html"

    def __init__(self, questionnaire_title, **kwargs):
        """Get questionnaire title."""
        self.questionnaire_title = questionnaire_title
        super().__init__(**kwargs)

    def get_context_data(self):
        """Return a context object for the template."""
        return {
            "questionnaire_title": self.questionnaire_title,
        }


class ResponseAlertEmail(BaseEmailMessage):
    """Email for response creation alerts."""

    template_name = "email/response_alert.html"

    def __init__(self, questionnaire_title, recipient, respondent, **kwargs):
        """Get email information."""
        self.questionnaire_title = questionnaire_title
        self.recipient = recipient
        self.respondent = respondent
        super().__init__(**kwargs)

    def get_context_data(self):
        """Return a context object for the template."""
        return {
            "questionnaire_title": self.questionnaire_title,
            "recipient": self.recipient,
            "respondent": self.respondent,
        }
