# Generated by Django 4.1 on 2023-04-27 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "cat_hotel_admin",
            "0003_remove_event_date_event_end_date_event_start_date_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="is_closed_for_holiday",
            field=models.BooleanField(default=False, null=True),
        ),
    ]
