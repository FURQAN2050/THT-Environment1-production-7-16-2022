# Generated by Django 2.2.2 on 2020-05-27 18:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0059_auto_20200527_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaaccount',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 27, 18, 55, 6, 772480, tzinfo=utc)),
        ),
    ]
