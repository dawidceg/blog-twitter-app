# Generated by Django 3.0.3 on 2020-05-01 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200501_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='activated',
            field=models.BooleanField(default=False),
        ),
    ]
