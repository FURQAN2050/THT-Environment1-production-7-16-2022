# Generated by Django 2.2.2 on 2019-09-30 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentationpage', '0005_auto_20190929_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentationpage',
            name='textContact',
            field=models.TextField(default=None, help_text='Enter section text'),
        ),
    ]
