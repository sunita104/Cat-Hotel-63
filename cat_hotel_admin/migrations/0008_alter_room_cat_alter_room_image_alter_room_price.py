# Generated by Django 4.1 on 2023-05-16 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cat_hotel_admin", "0007_alter_room_cat"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="cat",
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name="room",
            name="image",
            field=models.FileField(blank=True, null=True, upload_to="rooms/image"),
        ),
        migrations.AlterField(
            model_name="room", name="price", field=models.IntegerField(null=True),
        ),
    ]
