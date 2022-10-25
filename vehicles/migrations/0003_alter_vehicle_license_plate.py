# Generated by Django 4.1.2 on 2022-10-25 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0002_remove_shiftvehicle_shift_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicle",
            name="license_plate",
            field=models.CharField(
                db_index=True,
                help_text="License plat for this vehicle",
                max_length=255,
                verbose_name="License plate",
            ),
        ),
    ]
