# Generated by Django 5.0.4 on 2024-11-11 20:03

import antivienas.database.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_user_selected_avatar_alter_order_confirmation_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='default_img',
            field=models.ImageField(default='/user-no-avatar.png', upload_to=antivienas.database.models.user_img_upload_path),
        ),
        migrations.AlterField(
            model_name='order',
            name='confirmation_code',
            field=models.SmallIntegerField(default=7318),
        ),
        migrations.AlterField(
            model_name='user',
            name='img_one',
            field=models.ImageField(blank=True, null=True, upload_to=antivienas.database.models.user_img_upload_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='selected_avatar',
            field=models.SmallIntegerField(default=0),
        ),
    ]
