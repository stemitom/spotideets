import factory
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from factory.django import DjangoModelFactory

from apps.spotify.models import Album, Artist, Genre, SpotifyToken, Track, UserFavorite

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")


class SpotifyTokenFactory(DjangoModelFactory):
    class Meta:
        model = SpotifyToken

    user = factory.SubFactory(UserFactory)
    access_token = factory.Faker("text", max_nb_chars=1000)
    refresh_token = factory.Faker("text", max_nb_chars=1000)
    token_type = factory.Faker("text", max_nb_chars=100)
    expires_in = factory.Faker("pyint")
    created_at = factory.Faker("date_time_this_decade")


class GenreFactory(DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Faker("word")


class ArtistFactory(DjangoModelFactory):
    class Meta:
        model = Artist

    name = factory.Faker("name")


class AlbumFactory(DjangoModelFactory):
    class Meta:
        model = Album

    title = factory.Faker("sentence")


class TrackFactory(DjangoModelFactory):
    class Meta:
        model = Track

    title = factory.Faker("sentence")


class UserFavoriteFactory(DjangoModelFactory):
    class Meta:
        model = UserFavorite

    user = factory.SubFactory(UserFactory)
    track = factory.SubFactory(TrackFactory)


def test_spotify_token_model():
    user = UserFactory()
    token = SpotifyTokenFactory(user=user)
    assert token.user == user
    assert token.access_token != ""
    assert token.refresh_token != ""
    assert token.token_type != ""
    assert token.expires_in > 0
    assert token.expires_in > 0
    assert token.created_at <= timezone.now()


@pytest.mark.django_db
def test_genre_model():
    genre = GenreFactory(name="Rock")
    assert genre.name == "Rock"


@pytest.mark.django_db
def test_artist_model():
    artist = ArtistFactory(name="John Doe")
    assert artist.name == "John Doe"


@pytest.mark.django_db
def test_album_model():
    album = AlbumFactory(title="Greatest Hits")
    assert album.title == "Greatest Hits"


@pytest.mark.django_db
def test_track_model():
    track = TrackFactory(title="Song Title")
    assert track.title == "Song Title"


@pytest.mark.django_db
def test_user_favorite_model():
    user = UserFactory()
    track = TrackFactory()
    favorite = UserFavoriteFactory(user=user, track=track)
    assert favorite.user == user
    assert favorite.track == track
