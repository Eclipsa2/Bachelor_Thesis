# Generated by Django 4.2.9 on 2024-01-16 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0004_alter_chatsession_request_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="RequiredEntities",
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
                ("nume", models.BooleanField()),
                ("program_studii", models.BooleanField()),
                ("grupa", models.BooleanField()),
                ("an_studii", models.BooleanField()),
                ("forma_invatamant", models.BooleanField()),
                ("mentiuni", models.BooleanField()),
                ("titlu_licenta", models.BooleanField()),
                ("titlu_program_studii", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="ChatEntities",
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
                ("nume", models.CharField(default="", max_length=100)),
                ("program_studii", models.CharField(default="", max_length=100)),
                ("grupa", models.CharField(default="", max_length=100)),
                ("an_studii", models.CharField(default="", max_length=100)),
                ("forma_invatamant", models.CharField(default="", max_length=100)),
                ("mentiuni", models.CharField(default="", max_length=500)),
                ("titlu_licenta", models.CharField(default="", max_length=100)),
                ("titlu_program_studii", models.CharField(default="", max_length=100)),
                (
                    "chat_session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="website.chatsession",
                    ),
                ),
            ],
        ),
    ]
