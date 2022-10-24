# Generated by Django 4.1.2 on 2022-10-24 20:30

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("vehicles", "0002_remove_shiftvehicle_shift_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Shift",
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
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "shift_date",
                    models.DateField(
                        default=datetime.date.today,
                        help_text="Date for this shift.",
                        verbose_name="Shift date",
                    ),
                ),
                (
                    "employee",
                    models.IntegerField(
                        default=0,
                        help_text="Employee (ID) responsible for this shift.",
                        verbose_name="Employee",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ShiftVehicle",
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
                (
                    "order",
                    models.IntegerField(
                        help_text="What order to visit vehicles for this shift.",
                        verbose_name="Order",
                    ),
                ),
                (
                    "shift",
                    models.ForeignKey(
                        help_text="Vehicle is assigned to this shift.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shifts.shift",
                        verbose_name="Shift",
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        help_text="Vehicle is assigned to this shift.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vehicles.vehicle",
                        verbose_name="Vehicle",
                    ),
                ),
            ],
            options={
                "verbose_name": "Shift Vehicle Mapping",
                "verbose_name_plural": "Shift Vehicle Mappings",
                "ordering": ["order"],
            },
        ),
        migrations.AddField(
            model_name="shift",
            name="vehicles",
            field=models.ManyToManyField(
                blank=True,
                help_text="Vehicles of this shift.",
                related_name="shifts",
                through="shifts.ShiftVehicle",
                to="vehicles.vehicle",
                verbose_name="Vehicles",
            ),
        ),
    ]