# Generated by Django 4.1 on 2023-06-18 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cat_hotel", "0009_booking_confirm_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="email",
            field=models.EmailField(blank=True, max_length=50, null=True),
        ),
    ]