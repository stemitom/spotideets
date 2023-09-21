import requests
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.spotify.models import Artist, Genre, TimeFrame, TopArtists
from apps.spotify.serializers import ArtistSerializer


@method_decorator(login_required, name="dispatch")
class TopArtistsView(APIView):
    def get(self, request):
        access_token = request.user.spotifytoken.access_token
        headers = {"Authorization": f"Bearer {access_token}"}

        time_frame = request.GET.get("time_frame", "medium_term")
        time_frame_map = {
            "4 weeks": TimeFrame.SHORT_TERM,
            "6 months": TimeFrame.MEDIUM_TERM,
            "lifetime": TimeFrame.LONG_TERM,
        }
        time_frame = time_frame_map.get(time_frame, TimeFrame.MEDIUM_TERM)

        try:
            limit = int(request.GET.get("limit", 20))
        except ValueError:
            limit = 10

        response = requests.get(
            "https://api.spotify.com/v1/me/top/artists",
            headers=headers,
            params={"limit": limit, "time_range": time_frame.value},
        )

        if response.status_code == 200:
            top_artists_data = response.json().get("items", [])
            artists = []

            for order, artist_data in enumerate(top_artists_data):
                artist, _ = Artist.objects.get_or_create(
                    spotify_id=artist_data["id"],
                    defaults={
                        "name": artist_data["name"],
                    },
                )

                for genre_name in artist_data["genres"]:
                    genre, _ = Genre.objects.get_or_create(name=genre_name)
                    artist.genres.add(genre)

                artists.append(artist)

            Artist.objects.bulk_create(artists, ignore_conflicts=True)

            max_order = (
                TopArtists.objects.filter(user=request.user)
                .filter(time_frame=time_frame)
                .aggregate(max_order=Max("order"))
                .get("max_order")
                or 0
            )

            top_artists = [
                TopArtists(
                    user=request.user,
                    artist=artist,
                    time_frame=time_frame,
                    order=max_order + order + 1,
                )
                for order, artist in enumerate(artists)
            ]

            TopArtists.objects.bulk_create(top_artists)

            serializer = ArtistSerializer(artists, many=True)
            if request.accepted_renderer.format == "html":
                context = {"artists": serializer.data}
                return render(request, "top_artists.html", context)
            else:
                return Response(serializer.data)
        else:
            return Response(
                {"error": "Failed to retrieve top artists"}, status=response.status_code
            )
