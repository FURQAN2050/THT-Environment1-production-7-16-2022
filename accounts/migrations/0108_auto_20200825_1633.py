# Generated by Django 2.2.2 on 2020-08-25 16:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0107_auto_20200825_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaaccount',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 25, 16, 33, 20, 228144, tzinfo=utc)),
        ),
    ]
