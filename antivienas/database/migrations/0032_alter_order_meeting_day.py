# Generated by Django 5.0.4 on 2024-05-22 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0031_alter_order_meeting_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='meeting_day',
            field=models.DateField(),
        ),
    ]