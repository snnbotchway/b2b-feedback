# Generated by Django 4.1.7 on 2023-03-13 21:46

import django.db.models.deletion
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
                ("month", models.CharField(max_length=7)),
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
        ),
        migrations.AddConstraint(
            model_name="monthlyfeedback",
            constraint=models.UniqueConstraint(
                fields=("client_rep", "month"), name="unique_monthly_feedback"
            ),
        ),
    ]