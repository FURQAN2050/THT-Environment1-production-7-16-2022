# Generated by Django 2.2.2 on 2020-03-17 16:06

import accounts.models
import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0039_auto_20200316_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageBefore',
            fields=[
                ('mediaaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.MediaAccount')),
                ('image_field', models.ImageField(upload_to=accounts.models.user_directory_path)),
            ],
            options={
                'abstract': False,
            },
            bases=('accounts.mediaaccount',),
        ),
        migrations.CreateModel(
            name='ImageCurrent',
            fields=[
                ('mediaaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.MediaAccount')),
                ('image_field', models.ImageField(upload_to=accounts.models.user_directory_path)),
            ],
            options={
                'abstract': False,
            },
            bases=('accounts.mediaaccount',),
        ),
        migrations.AlterField(
            model_name='mediaaccount',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 17, 16, 6, 14, 934724, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='teacher',
            name='beforePicture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.ImageBefore'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='currentPicture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.ImageCurrent'),
        ),
    ]
