# Generated by Django 4.2.7 on 2024-01-23 07:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount_code', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcode',
            name='discount_percent',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
