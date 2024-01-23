# Generated by Django 5.0 on 2024-01-06 00:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_initial'),
        ('user', '0003_customuser_password_reset_token_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='user.customuser'),
        ),
    ]
