# Generated by Django 5.1.3 on 2024-11-13 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Produkt",
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
                ("model", models.CharField(max_length=100, unique=True)),
                ("stawka", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
