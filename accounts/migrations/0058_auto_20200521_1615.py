# Generated by Django 2.2.2 on 2020-05-21 20:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0057_auto_20200521_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaaccount',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 21, 20, 15, 30, 5204, tzinfo=utc)),
        ),
    ]
