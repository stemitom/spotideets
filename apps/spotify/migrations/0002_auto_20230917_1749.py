# Generated by Django 3.2.10 on 2023-09-17 17:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("spotify", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="spotifytoken",
            name="access_token",
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name="spotifytoken",
            name="refresh_token",
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name="spotifytoken",
            name="token_type",
            field=models.CharField(max_length=100),
        ),
    ]
