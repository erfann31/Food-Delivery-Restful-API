# Generated by Django 5.0 on 2023-12-30 00:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('stars', models.FloatField(default=0)),
                ('stars_count', models.IntegerField(default=0)),
                ('min_time_to_delivery', models.IntegerField(default=0)),
                ('max_time_to_delivery', models.IntegerField(default=0)),
                ('category', models.CharField(choices=[('Burger', 'Burger'), ('Pizza', 'Pizza'), ('Chicken', 'Chicken'), ('Fish', 'Fish'), ('Pie', 'Pie'), ('Asian', 'Asian'), ('Desserts', 'Desserts'), ('Skewers', 'Skewers'), ('Rice', 'Rice'), ('Vegetables', 'Vegetables'), ('Other', 'Other')], max_length=50)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant')),
            ],
        ),
    ]
