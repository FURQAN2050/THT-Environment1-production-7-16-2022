# Generated by Django 2.2.2 on 2019-08-06 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190724_1824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teams',
            options={'verbose_name_plural': 'Teams'},
        ),
        migrations.AlterField(
            model_name='user',
            name='isDistrictManager',
            field=models.BooleanField(default=False),
        ),
    ]
