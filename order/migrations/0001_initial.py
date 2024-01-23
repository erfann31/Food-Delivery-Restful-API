# Generated by Django 5.0 on 2024-01-01 04:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0002_initial'),
        ('discount_code', '0001_initial'),
        ('food', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed')], default='Ongoing', max_length=20)),
                ('date_and_time', models.DateTimeField(auto_now_add=True)),
                ('estimated_arrival', models.IntegerField(choices=[(20, '20 minutes'), (21, '21 minutes'), (22, '22 minutes'), (23, '23 minutes'), (24, '24 minutes'), (25, '25 minutes'), (26, '26 minutes'), (27, '27 minutes'), (28, '28 minutes'), (29, '29 minutes'), (30, '30 minutes'), (31, '31 minutes'), (32, '32 minutes'), (33, '33 minutes'), (34, '34 minutes'), (35, '35 minutes'), (36, '36 minutes'), (37, '37 minutes'), (38, '38 minutes'), (39, '39 minutes'), (40, '40 minutes'), (41, '41 minutes'), (42, '42 minutes'), (43, '43 minutes'), (44, '44 minutes'), (45, '45 minutes'), (46, '46 minutes'), (47, '47 minutes'), (48, '48 minutes'), (49, '49 minutes'), (50, '50 minutes'), (51, '51 minutes'), (52, '52 minutes'), (53, '53 minutes'), (54, '54 minutes'), (55, '55 minutes'), (56, '56 minutes'), (57, '57 minutes'), (58, '58 minutes'), (59, '59 minutes'), (60, '60 minutes'), (61, '61 minutes'), (62, '62 minutes'), (63, '63 minutes'), (64, '64 minutes'), (65, '65 minutes'), (66, '66 minutes'), (67, '67 minutes'), (68, '68 minutes'), (69, '69 minutes'), (70, '70 minutes'), (71, '71 minutes'), (72, '72 minutes'), (73, '73 minutes'), (74, '74 minutes'), (75, '75 minutes'), (76, '76 minutes'), (77, '77 minutes'), (78, '78 minutes'), (79, '79 minutes'), (80, '80 minutes'), (81, '81 minutes'), (82, '82 minutes'), (83, '83 minutes'), (84, '84 minutes'), (85, '85 minutes'), (86, '86 minutes'), (87, '87 minutes'), (88, '88 minutes'), (89, '89 minutes'), (90, '90 minutes')])),
                ('is_canceled', models.BooleanField(default=False)),
                ('delivery_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='address.address')),
                ('discount_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='discount_code.discountcode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.food')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
    ]