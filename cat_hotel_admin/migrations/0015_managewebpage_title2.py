# Generated by Django 4.1 on 2023-07-12 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cat_hotel_admin", "0014_remove_managewebpage_image3_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="managewebpage",
            name="title2",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
