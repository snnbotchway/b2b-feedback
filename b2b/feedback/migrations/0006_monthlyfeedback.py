# Generated by Django 4.1.7 on 2023-03-13 23:19

import django.db.models.deletion
import feedback.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "feedback",
            "0005_questionnaire_author_alter_questionnaire_client_rep_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="MonthlyFeedback",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "month",
                    models.CharField(
                        default="2023-03",
                        max_length=7,
                        validators=[feedback.validators.validate_month_format],
                    ),
                ),
                ("feedback", models.TextField()),
                (
                    "client_rep",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to={
                            "groups__name": "Corporate Client Representatives"
                        },
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="monthly_feedback",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Monthly feedback",
            },
        ),
    ]
