# Generated by Django 4.2.3 on 2024-09-07 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songmodel',
            name='song_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
