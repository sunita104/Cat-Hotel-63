# Generated by Django 4.1 on 2023-07-12 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cat_hotel_admin", "0011_incomesummary_delete_revenuedata"),
    ]

    operations = [
        migrations.CreateModel(
            name="ManageWebpage",
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
                ("title", models.TextField(max_length=255, null=True)),
                ("image1", models.ImageField(null=True, upload_to="slideshow_images/")),
                ("image2", models.ImageField(null=True, upload_to="slideshow_images/")),
                ("image3", models.ImageField(null=True, upload_to="slideshow_images/")),
                ("description1", models.TextField(max_length=255, null=True)),
                (
                    "image4",
                    models.ImageField(null=True, upload_to="recommended_images/"),
                ),
                ("description2", models.TextField(max_length=255, null=True)),
                ("about_us", models.TextField(max_length=255, null=True)),
                ("location", models.TextField(max_length=255, null=True)),
                ("contact", models.TextField(max_length=255, null=True)),
            ],
        ),
    ]
