# Generated by Django 3.2.10 on 2023-09-21 16:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("spotify", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="spotifytoken",
            name="expires_in",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="userfavorite",
            name="user",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
