# Generated by Django 2.2.2 on 2020-05-28 22:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0070_auto_20200528_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaaccount',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 28, 22, 5, 35, 814006, tzinfo=utc)),
        ),
    ]
