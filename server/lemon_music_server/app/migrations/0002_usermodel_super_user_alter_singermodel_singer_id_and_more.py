# Generated by Django 4.2.3 on 2023-12-10 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='super_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='singermodel',
            name='singer_id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='songmodel',
            name='media_type',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
