# Generated by Django 2.2.2 on 2020-08-05 19:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0075_auto_20200606_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaaccount',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 5, 19, 23, 10, 293290, tzinfo=utc)),
        ),
    ]
