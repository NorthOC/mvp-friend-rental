# Generated by Django 5.0.4 on 2024-05-19 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0020_friendsetting_profit_per_hour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendsetting',
            name='profit_per_hour',
        ),
    ]
