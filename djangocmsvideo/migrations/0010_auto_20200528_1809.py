# Generated by Django 2.2.2 on 2020-05-28 22:09

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocmsvideo', '0009_auto_20200528_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='caption',
            field=tinymce.models.HTMLField(blank=True, default='', null=True),
        ),
    ]
