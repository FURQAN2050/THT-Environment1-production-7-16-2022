# Generated by Django 2.2.2 on 2020-08-21 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workoutgames', '0022_movementtype_thumbnail_movement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movementtype',
            name='image_content',
        ),
        migrations.RemoveField(
            model_name='movementtype',
            name='thumbnail_movement',
        ),
        migrations.RemoveField(
            model_name='movementtype',
            name='video_content',
        ),
    ]
