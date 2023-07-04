# Generated by Django 4.1 on 2023-06-18 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cat_hotel", "0011_alter_booking_customer_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                ("name", models.CharField(max_length=50, null=True)),
                ("username", models.CharField(max_length=50, null=True)),
                ("email", models.EmailField(blank=True, max_length=50, null=True)),
                ("password", models.CharField(max_length=7, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name="booking",
            name="customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="cat_hotel.customer",
            ),
        ),
        migrations.AlterField(
            model_name="bookinghistory",
            name="customer_b",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="cat_hotel.customer",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="cat_hotel.customer",
            ),
        ),
    ]