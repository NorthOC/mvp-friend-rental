# Generated by Django 5.0.4 on 2024-11-11 17:27

import antivienas.database.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_alter_order_confirmation_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='selected_avatar',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='confirmation_code',
            field=models.SmallIntegerField(default=6232),
        ),
        migrations.AlterField(
            model_name='user',
            name='img_one',
            field=models.ImageField(default='/user-no-avatar.png', upload_to=antivienas.database.models.user_img_upload_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='img_three',
            field=models.ImageField(blank=True, null=True, upload_to=antivienas.database.models.user_img_upload_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='img_two',
            field=models.ImageField(blank=True, null=True, upload_to=antivienas.database.models.user_img_upload_path),
        ),
    ]
