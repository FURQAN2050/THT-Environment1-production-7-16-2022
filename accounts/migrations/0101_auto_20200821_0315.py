# Generated by Django 2.2.2 on 2020-08-21 03:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0100_auto_20200821_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaaccount',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 21, 3, 15, 51, 303105, tzinfo=utc)),
        ),
    ]
