# Generated by Django 5.0.4 on 2024-05-20 08:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0029_alter_order_meeting_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(default=datetime.date(1998, 5, 14)),
        ),
    ]