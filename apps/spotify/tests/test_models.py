import factory
import pytest
from factory.django import DjangoModelFactory

from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.spotify.models import Album, Artist, Genre, SpotifyToken, Track

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


@pytest.mark.django_db
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
