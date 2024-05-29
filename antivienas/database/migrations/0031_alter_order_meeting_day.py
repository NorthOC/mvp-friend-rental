# Generated by Django 5.0.4 on 2024-05-22 11:01

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0030_alter_user_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='meeting_day',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2024, 5, 22))]),
        ),
    ]
