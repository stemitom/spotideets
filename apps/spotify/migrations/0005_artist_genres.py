# Generated by Django 3.2.10 on 2023-09-21 21:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("spotify", "0004_artist_popularity"),
    ]

    operations = [
        migrations.AddField(
            model_name="artist",
            name="genres",
            field=models.ManyToManyField(to="spotify.Genre"),
        ),
    ]