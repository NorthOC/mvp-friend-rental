# Generated by Django 5.0.4 on 2024-05-19 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0019_order_cancel_reason_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendsetting',
            name='profit_per_hour',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
