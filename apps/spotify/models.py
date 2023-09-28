from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from commons.models import TimeAndUUIDStampedBaseModel, TopCharacteristics

User = get_user_model()


class SpotifyToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=1000)
    refresh_token = models.CharField(max_length=1000)
    token_type = models.CharField(max_length=100)
    expires_in = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

    def is_token_expired(self):
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        self.expires_at = timezone.now() + timezone.timedelta(
            seconds=self.expires_in,
        )
        super().save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Artist(models.Model):
    artist_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    spotify_popularity = models.PositiveIntegerField(default=0)
    genres = models.ManyToManyField(Genre)
    followers_count = models.IntegerField(default=0)
    image_url = models.URLField()

    def __str__(self):
        return self.name


class TopArtists(Artist, TopCharacteristics):
    pass


class Album(models.Model):
    album_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.URLField()
    release_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class TopAlbums(Album, TopCharacteristics):
    pass


class Track(TimeAndUUIDStampedBaseModel):
    song_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    img_url = models.URLField()
    artists = models.ManyToManyField(Artist, related_name="tracks")
    albums = models.ManyToManyField(Album, related_name="tracks")
    duration_ms = models.PositiveBigIntegerField(default=0)
    spotify_popularity = models.IntegerField(default=0)
    spotify_preview = models.URLField()
    explicit = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TopTracks(TopCharacteristics):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.OneToOneField(Track, on_delete=models.CASCADE)


class Follower(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="followers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"{self.user.username} follows {self.artist.name}"
