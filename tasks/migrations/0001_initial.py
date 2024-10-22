# Generated by Django 5.1.2 on 2024-10-17 14:15

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
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
                ("task_type", models.CharField(max_length=25)),
                ("payload", models.TextField()),
                ("status", models.CharField(max_length=20)),
                ("statuslog", models.CharField(max_length=255)),
                ("retries", models.IntegerField()),
                ("priority", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("processed_at", models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
