# Generated by Django 3.2.10 on 2023-10-05 08:18

import commons.enums
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import enumfields.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('image', models.URLField()),
                ('release_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('artist_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('spotify_popularity', models.PositiveIntegerField(default=0)),
                ('followers_count', models.IntegerField(default=0)),
                ('image_url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('song_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('img_url', models.URLField()),
                ('duration_ms', models.PositiveBigIntegerField(default=0)),
                ('spotify_popularity', models.IntegerField(default=0)),
                ('spotify_preview', models.URLField(null=True)),
                ('explicit', models.BooleanField(default=False)),
                ('albums', models.ManyToManyField(related_name='tracks', to='spotify.Album')),
                ('artists', models.ManyToManyField(related_name='tracks', to='spotify.Artist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TopTracks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=1)),
                ('streams', models.PositiveIntegerField(default=1)),
                ('indicator', enumfields.fields.EnumField(default='same', enum=commons.enums.IndicatorEnum, max_length=20)),
                ('timeframe', enumfields.fields.EnumField(enum=commons.enums.TimeFrame, max_length=20)),
                ('track', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='spotify.track')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TopGenres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=1)),
                ('streams', models.PositiveIntegerField(default=1)),
                ('indicator', enumfields.fields.EnumField(default='same', enum=commons.enums.IndicatorEnum, max_length=20)),
                ('timeframe', enumfields.fields.EnumField(enum=commons.enums.TimeFrame, max_length=20)),
                ('genre', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='spotify.genre')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TopArtists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=1)),
                ('streams', models.PositiveIntegerField(default=1)),
                ('indicator', enumfields.fields.EnumField(default='same', enum=commons.enums.IndicatorEnum, max_length=20)),
                ('timeframe', enumfields.fields.EnumField(enum=commons.enums.TimeFrame, max_length=20)),
                ('artist', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='spotify.artist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SpotifyToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=1000)),
                ('refresh_token', models.CharField(max_length=1000)),
                ('token_type', models.CharField(max_length=100)),
                ('expires_in', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expires_at', models.DateTimeField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='spotify.artist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='artist',
            name='genres',
            field=models.ManyToManyField(to='spotify.Genre'),
        ),
    ]
