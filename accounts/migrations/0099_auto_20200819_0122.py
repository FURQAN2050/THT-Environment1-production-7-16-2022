# Generated by Django 2.2.2 on 2020-08-19 01:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0098_auto_20200818_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaaccount',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 19, 1, 22, 40, 561766, tzinfo=utc)),
        ),
    ]
