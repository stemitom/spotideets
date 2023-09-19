import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.spotify.models import Track, TopTracks, Genre, Artist
from apps.spotify.serializers import TrackSerializer



class TopTracksView(APIView):
    def get(self, request):
        access_token = request.user.spotifytoken.access_token

        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(
            "https://api.spotify.com/v1/me/top/tracks", headers=headers
        )

        if response.status_code == 200:
            top_tracks_data = response.json().get("items", [])
            tracks = []

            for order, track_data in enumerate(top_tracks_data):
                track, _ = Track.objects.get_or_create(
                    song_id=track_data["id"],
                    defaults={
                        "name": track_data["name"],
                        "img_url": track_data["album"]["images"][0]["url"],
                    },
                )

                if track.img_url != track_data["album"]["images"][0]["url"]:
                    track.img_url = track_data["album"]["images"][0]["url"]
                    track.save()

                for genre_data in track_data["genres"]:
                    genre, _ = Genre.objects.get_or_create(name=genre_data)
                    track.genres.add(genre)

                for artist_data in track_data["artists"]:
                    artist, _ = Artist.objects.get_or_create(
                        artist_id=artist_data["id"], name=artist_data["name"]
                    )
                    track.artists.add(artist)

                tracks.append(track)

            Track.objects.bulk_create(tracks)

            # Get the maximum order for the user and time_frame
            max_order = (
                TopTracks.objects.filter(user=request.user)
                .filter(time_frame=TimeFrame.MEDIUM_TERM)  # Replace with the desired time_frame
                .aggregate(Max("order"))
                .get("order__max", 0)
            )

            top_tracks = [
                TopTracks(
                    user=request.user,
                    track=track,
                    time_frame=TimeFrame.MEDIUM_TERM,  # Replace with the desired time_frame
                    order=max_order + order + 1,
                )
                for order, track in enumerate(tracks)
            ]

            TopTracks.objects.bulk_create(top_tracks)

            serializer = TrackSerializer(tracks, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Failed to retrieve top tracks"}, status=response.status_code
            )