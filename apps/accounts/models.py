from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    spotify_user_email = models.EmailField(unique=True, blank=False, null=False)
    spotify_user_id = models.CharField(max_length=255, unique=True, blank=False, null=False)
    bio = models.TextField(
        max_length=255,
        blank=True,
        null=True,
        default="Hey, I'm using spotideets",
    )
    display_name = models.CharField(max_length=255, null=True)
    custom_url = models.URLField(max_length=255, null=True)

    def __str__(self) -> str:
        return f"{self.spotify_user_id}"

    def save(self, *args, **kwargs):
        if not self.custom_url or self.username != CustomUser.objects.get(pk=self.pk).username:
            self.custom_url = f'http://localhost:8000/{self.username}'

        super().save(*args, **kwargs)


class PrivacySettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    show_streams = models.BooleanField(default=True)
    show_leaderboards = models.BooleanField(default=True)
    show_friends = models.BooleanField(default=True)
    show_public_profile = models.BooleanField(default=True)
    show_current_playing = models.BooleanField(default=True)
    show_recently_played = models.BooleanField(default=True)
    show_top_tracks = models.BooleanField(default=True)
    show_top_genres = models.BooleanField(default=True)
    show_top_albums = models.BooleanField(default=True)
    show_connections = models.BooleanField(default=True)
    show_top_artists = models.BooleanField(default=True)
    show_streams_stats = models.BooleanField(default=True)


class Friendship(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friendships")
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friend_of")

    def __str__(self):
        return f"{self.user} - {self.friend}"
