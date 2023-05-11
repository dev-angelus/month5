# Generated by Django 4.2.1 on 2023-05-11 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0003_genre_alter_movie_director_alter_movie_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(blank=True, to='movie_app.genre'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_app.director'),
        ),
    ]
