# Generated by Django 2.2.2 on 2020-05-28 15:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0064_auto_20200528_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaaccount',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 28, 15, 14, 44, 755908, tzinfo=utc)),
        ),
    ]
