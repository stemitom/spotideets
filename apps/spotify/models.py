from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from enumfields import EnumField

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
    spotify_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    popularity = models.PositiveIntegerField(default=0)
    genres = models.ManyToManyField(Genre)
    top_tracks = models.ManyToManyField("Track", related_name="top_artists")
    top_albums = models.ManyToManyField("Album", related_name="top_artists")
    top_listeners = models.ManyToManyField(User, related_name="top_artists")

    def __str__(self):
        return self.name


class Album(models.Model):
    album_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    release_date = models.DateField()

    def __str__(self):
        return self.name


class Track(models.Model):
    song_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    img_url = models.URLField()
    genres = models.ManyToManyField(Genre, related_name="tracks")
    artists = models.ManyToManyField(Artist, related_name="tracks")
    albums = models.ManyToManyField(Album, related_name="tracks")

    def __str__(self):
        return self.name


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_tracks = models.ManyToManyField(Track, related_name="favorited_by")
    favorite_artists = models.ManyToManyField(Artist, related_name="favorited_by")
    favorite_genres = models.ManyToManyField(Genre, related_name="favorited_by")

    def __str__(self):
        return self.user.username


class Follower(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="followers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"{self.user.username} follows {self.artist.name}"


class TimeFrame(Enum):
    LONG_TERM = "long_term"
    MEDIUM_TERM = "medium_term"
    SHORT_TERM = "short_term"


class TopTracks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    time_frame = EnumField(TimeFrame, max_length=50)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.track.name} ({self.time_frame})"


class TopGenres(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    time_frame = EnumField(TimeFrame, max_length=50)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.genre.name} ({self.time_frame})"


class TopArtists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    time_frame = EnumField(TimeFrame, max_length=50)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.artist.name} ({self.time_frame})"
