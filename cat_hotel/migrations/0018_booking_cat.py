# Generated by Django 4.1 on 2023-07-24 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cat_hotel", "0017_remove_cancellationreason_booking_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="cat",
            field=models.IntegerField(default=1, null=True),
        ),
    ]
