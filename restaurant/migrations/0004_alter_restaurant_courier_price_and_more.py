# Generated by Django 4.2.7 on 2024-01-23 07:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_alter_restaurant_distance_alter_restaurant_stars_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='courier_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999999)]),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='distance',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='opening_time',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)]),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='stars',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='stars_count',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]