from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    spotify_user_email = models.EmailField(unique=True)
    spotify_user_id = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.spotify_user_id}"


class PrivacySettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    public_profile = models.BooleanField(default=True)
    current_playing = models.BooleanField(default=True)
    recently_played = models.BooleanField(default=True)
    show_top_tracks = models.BooleanField(default=True)
    show_top_artists = models.BooleanField(default=True)
    show_top_genres = models.BooleanField(default=True)
    show_top_albums = models.BooleanField(default=True)
    show_streams = models.BooleanField(default=True)
    show_streams_stats = models.Boolean(default=True)
    leaderboards = models.BooleanField(default=True)
    show_friends = models.BooleanField(default=True)
    show_connections = models.BooleanField(default=True)
