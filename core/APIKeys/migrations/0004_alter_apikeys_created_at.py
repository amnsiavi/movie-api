# Generated by Django 5.0.7 on 2024-08-06 11:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIKeys', '0003_alter_apikeys_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikeys',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 6, 11, 20, 20, 263019)),
        ),
    ]