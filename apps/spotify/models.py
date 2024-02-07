from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from apps import spotify

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


class TopGenres(TopCharacteristics):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.OneToOneField(Genre, on_delete=models.CASCADE)


class Artist(TimeAndUUIDStampedBaseModel):
    spotify_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    spotify_popularity = models.PositiveIntegerField(default=0)
    genres = models.ManyToManyField(Genre)
    followers_count = models.IntegerField(default=0)
    img_url = models.URLField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class TopArtists(TopCharacteristics):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)


class Album(models.Model):
    spotify_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.URLField()
    release_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Track(TimeAndUUIDStampedBaseModel):
    spotify_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    img_url = models.URLField()
    artists = models.ManyToManyField(Artist, related_name="tracks")
    albums = models.ManyToManyField(Album, related_name="tracks")
    duration_ms = models.PositiveBigIntegerField(default=0)
    spotify_popularity = models.IntegerField(default=0)
    spotify_preview_url = models.URLField(null=True)
    explicit = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TopTracks(TopCharacteristics):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.OneToOneField(Track, on_delete=models.CASCADE)


class UserArtistRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="artist_relations")
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="user_relations")
    position = models.IntegerField()
    indicator = models.CharField(max_length=10, blank=True, null=True)  # "UP", "DOWN", "NEW", or None
    date = models.DateField(default=timezone.now)


class UserTrackRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="track_relations")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="user_relations")
    position = models.IntegerField()
    indicator = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateField(default=timezone.now)


class ArtistPopularityHistory(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="popularity_history")
    popularity = models.PositiveIntegerField()
    date_recorded = models.DateField(default=timezone.now)

    class Meta:
        get_latest_by = "date_recorded"
