# Generated by Django 4.2.2 on 2023-07-06 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_picture'),
        ),
    ]
