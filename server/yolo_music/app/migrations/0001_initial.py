# Generated by Django 4.2.15 on 2024-09-01 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArtistModel',
            fields=[
                ('artist_id', models.AutoField(primary_key=True, serialize=False)),
                ('artist_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SongModel',
            fields=[
                ('song_id', models.IntegerField(primary_key=True, serialize=False)),
                ('song_name', models.CharField(max_length=255)),
                ('duration', models.IntegerField()),
                ('media_type', models.IntegerField()),
                ('sq_file_name', models.CharField(max_length=255)),
                ('sq_file_path', models.CharField(max_length=255)),
                ('hq_file_name', models.CharField(max_length=255)),
                ('hq_file_path', models.CharField(max_length=255)),
                ('cover_path', models.CharField(default='', max_length=255)),
                ('added_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Song2ArtistModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.artistmodel')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.songmodel')),
            ],
        ),
    ]