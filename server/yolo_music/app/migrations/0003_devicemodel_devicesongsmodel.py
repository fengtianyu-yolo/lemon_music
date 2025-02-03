# Generated by Django 4.2.3 on 2025-02-03 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_songmodel_song_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('device_id', models.AutoField(primary_key=True, serialize=False)),
                ('device_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceSongsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_time', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.devicemodel')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.songmodel')),
            ],
        ),
    ]
