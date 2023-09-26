from collections import Counter

from django.contrib.auth.decorators import login_required
from django.db.models import Max
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
            artist, _ = Artist.objects.get_or_create(
                spotify_id=artist_data["id"],
                defaults={
                    "name": artist_data["name"],
                },
            )

            for genre_name in artist_data["genres"]:
                genre, _ = Genre.objects.get_or_create(name=genre_name)
                artist.genres.add(genre)
                genre_counter[genre_name] += 1

            artists.append(artist)

        Artist.objects.bulk_create(artists, ignore_conflicts=True)

        top_genres = [Genre.objects.get_or_create(name=genre_name)[0] for genre_name in genre_counter.keys()]

        max_order = (
            TopArtists.objects.filter(user=self.request.user)
            .filter(time_frame=time_frame)
            .aggregate(max_order=Max("order"))
            .get("max_order")
            or 0
        )

        top_artists = [
            TopArtists(
                user=self.request.user,
                artist=artist,
                time_frame=time_frame,
                order=max_order + order + 1,
            )
            for order, artist in enumerate(artists)
        ]

        TopArtists.objects.bulk_create(top_artists)

        artist_serializer = ArtistSerializer(artists, many=True)
        genre_serializer = GenreSerializer(top_genres, many=True)
        return Response(
            {
                "artist": artist_serializer.data,
                "top_genres": genre_serializer.data,
            }
        )
