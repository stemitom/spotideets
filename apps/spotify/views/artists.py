from collections import Counter

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework.response import Response

from apps.spotify.models import Artist, Genre, TopArtists
from apps.spotify.serializers import ArtistSerializer, GenreSerializer
from apps.spotify.views.base import SpotifyAPIView


@method_decorator(login_required, name="dispatch")
class TopArtistsView(SpotifyAPIView):
    spotify_endpoint = "https://api.spotify.com/v1/me/top/artists"

    def handle_response(self, response, time_frame):
        top_artists_data = response.json().get("items", [])
        artists = []

        genre_counter = Counter()

        for _, artist_data in enumerate(top_artists_data):
            artist, _ = Artist.objects.update_or_create(
                artist_id=artist_data["id"],
                defaults={
                    "name": artist_data["name"],
                },
            )

            genres = [Genre.objects.get_or_create(name=genre_name)[0] for genre_name in artist_data["genres"]]
            artist.genres.set(genres)
            genre_counter.update(genres)
            artists.append(artist)

        Artist.objects.bulk_create(artists, ignore_conflicts=True)

        genre_ids = Genre.objects.filter(name__in=genre_counter.keys()).values_list("id", flat=True)
        top_genres = [
            Genre.objects.get_or_create(id=genre_id, name=genre_name)[0]
            for genre_id, genre_name in zip(genre_ids, genre_counter.keys())
        ]

        top_artists = [
            TopArtists(
                user=self.request.user,
                artist=artist,
                timeframe=time_frame,
            )
            for artist in artists
        ]

        TopArtists.objects.filter(user=self.request.user, timeframe=time_frame).delete()
        for top_artist in top_artists:
            top_artist.save()

        for artist, top_artist in zip(artists, top_artists):
            top_artist.artist = artist

        TopArtists.objects.bulk_update(top_artists, ["artist"])

        artist_serializer = ArtistSerializer(artists, many=True)
        genre_serializer = GenreSerializer(top_genres, many=True)
        return Response(
            {
                "artist": artist_serializer.data,
                "top_genres": genre_serializer.data,
            }
        )
