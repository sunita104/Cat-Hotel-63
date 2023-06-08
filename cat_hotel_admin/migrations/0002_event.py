# Generated by Django 4.1 on 2023-04-20 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cat_hotel_admin", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("name", models.CharField(max_length=200)),
                ("date", models.DateField()),
                ("is_holiday", models.BooleanField(default=False)),
            ],
        ),
    ]
