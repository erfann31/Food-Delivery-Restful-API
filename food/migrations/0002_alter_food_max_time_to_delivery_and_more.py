# Generated by Django 4.2.7 on 2024-01-23 06:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='max_time_to_delivery',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(90)]),
        ),
        migrations.AlterField(
            model_name='food',
            name='min_time_to_delivery',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(15), django.core.validators.MaxValueValidator(75)]),
        ),
    ]