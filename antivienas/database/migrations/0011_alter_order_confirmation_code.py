# Generated by Django 5.0.4 on 2024-11-23 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0010_verifyidpicture_remove_user_id_img_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='confirmation_code',
            field=models.SmallIntegerField(default=4466),
        ),
    ]
