# Generated by Django 5.0.4 on 2024-05-18 21:20

import antivienas.database.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0014_alter_user_img_one'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='img_one',
            field=models.ImageField(default='/user-no-avatar.png', upload_to=antivienas.database.models.upload_img_one),
        ),
    ]