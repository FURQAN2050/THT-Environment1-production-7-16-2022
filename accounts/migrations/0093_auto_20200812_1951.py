# Generated by Django 2.2.2 on 2020-08-12 19:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0092_auto_20200812_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaaccount',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 12, 19, 51, 53, 722561, tzinfo=utc)),
        ),
    ]
