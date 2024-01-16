# Generated by Django 4.2.9 on 2024-01-16 14:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0002_chatsession_last_updated"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatsession",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="chatsession",
            name="request_type",
            field=models.IntegerField(default=0),
        ),
    ]