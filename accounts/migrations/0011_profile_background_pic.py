# Generated by Django 3.0.3 on 2020-05-19 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='background_pic',
            field=models.ImageField(blank=True, default='default_background.jpg', upload_to='profile_pics'),
        ),
    ]
