# Generated by Django 2.2.2 on 2020-05-04 16:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0047_auto_20200504_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaaccount',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 4, 16, 42, 10, 372826, tzinfo=utc)),
        ),
    ]
