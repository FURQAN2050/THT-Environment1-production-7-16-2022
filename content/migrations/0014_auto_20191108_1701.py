# Generated by Django 2.2.2 on 2019-11-08 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0013_auto_20191108_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
