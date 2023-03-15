# Generated by Django 4.1.7 on 2023-03-12 12:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feedback", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="questionnaire",
            name="client",
        ),
        migrations.AddField(
            model_name="questionnaire",
            name="client_rep",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"groups__name": "Corporate Client Representatives"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="questionnaires",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
