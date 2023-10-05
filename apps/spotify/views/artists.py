from collections import Counter

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework.response import Response

from apps.spotify.models import Artist, Genre, TopArtists, TopGenres
from apps.spotify.serializers import TopArtistsSerializer, TopGenresSerializer
from apps.spotify.util import calculate_indicator
from apps.spotify.views.base import SpotifyAPIView


@method_decorator(login_required, name="dispatch")
class TopArtistsView(SpotifyAPIView):
    spotify_endpoint = "https://api.spotify.com/v1/me/top/artists"

    def handle_response(self, response, time_frame):
        top_artists_data = response.json().get("items", [])
        artists = []
        positions = []

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
            positions.append(artist.artist_id)

        indicators = calculate_indicator(positions)
        print(indicators)
        Artist.objects.bulk_create(artists, ignore_conflicts=True)

        print(genre_counter)
        all_genres = Genre.objects.filter(name__in=genre_counter.keys())

        TopGenres.objects.filter(user=self.request.user, timeframe=time_frame).delete()
        top_genres = [
            TopGenres(
                user=self.request.user,
                genre=genre,
                timeframe=time_frame,
            )
            for genre in all_genres
        ]
        TopGenres.objects.bulk_create(top_genres, ignore_conflicts=True)

        TopArtists.objects.filter(user=self.request.user, timeframe=time_frame).delete()
        top_artists = [
            TopArtists(
                user=self.request.user,
                artist=artist,
                timeframe=time_frame,
            )
            for artist in artists
        ]

        TopArtists.objects.bulk_create(top_artists, ignore_conflicts=True)

        artist_serializer = TopArtistsSerializer(top_artists, many=True)
        genre_serializer = TopGenresSerializer(top_genres, many=True)
        return Response(
            {
                "artist": artist_serializer.data,
                "top_genres": genre_serializer.data,
            }
        )
