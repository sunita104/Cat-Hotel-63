# Generated by Django 4.1 on 2023-05-06 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cat_hotel", "0004_remove_booking_ended_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookinghistory",
            name="checked_out",
            field=models.BooleanField(default=False, null=True),
        ),
    ]
