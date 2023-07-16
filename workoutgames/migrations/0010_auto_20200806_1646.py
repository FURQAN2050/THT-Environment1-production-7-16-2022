# Generated by Django 2.2.2 on 2020-08-06 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workoutgames', '0009_gamer_accessedpath'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovementType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('datePosted', models.DateTimeField()),
                ('image_content', models.ManyToManyField(blank=True, to='workoutgames.ImageWorkout')),
                ('tag', models.ManyToManyField(to='workoutgames.Tag')),
                ('video_content', models.ManyToManyField(blank=True, to='workoutgames.VideoWorkout')),
            ],
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_reps', models.IntegerField(default=1)),
                ('base_sets', models.IntegerField(default=1)),
                ('base_weight', models.FloatField(default=1)),
                ('use_autocalculation_algorithm', models.BooleanField(default=True)),
                ('movement_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workoutgames.MovementType')),
            ],
        ),
        migrations.AddField(
            model_name='workout',
            name='movements',
            field=models.ManyToManyField(to='workoutgames.Movement'),
        ),
    ]
