from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.response import Response

from apps.spotify.models import Artist, TopTracks, Track
from apps.spotify.serializers import TrackSerializer
from apps.spotify.views.base import SpotifyAPIView


@method_decorator(login_required, name="dispatch")
class TopTracksView(SpotifyAPIView):
    spotify_endpoint = "https://api.spotify.com/v1/me/top/tracks"

    def handle_response(self, response, time_frame):
        top_tracks_data = response.json().get("items", [])
        tracks = []

        for _, track_data in enumerate(top_tracks_data):
            track, _ = Track.objects.get_or_create(
                song_id=track_data["id"],
                defaults={
                    "name": track_data["name"],
                    "img_url": track_data["album"]["images"][0]["url"],
                },
            )

            for artist_data in track_data["artists"]:
                artist, _ = Artist.objects.get_or_create(
                    artist_id=artist_data["id"],
                    defaults={
                        "name": artist_data["name"],
                    },
                )
                track.artists.add(artist)

            tracks.append(track)

        Track.objects.bulk_create(tracks, ignore_conflicts=True)
        TopTracks.objects.filter(user=self.request.user, time_frame=time_frame).delete()

        top_tracks = [
            TopTracks(
                user=self.request.user,
                track=track,
                time_frame=time_frame,
            )
            for track in tracks
        ]

        TopTracks.objects.bulk_create(top_tracks)

        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)


@method_decorator(login_required, name="dispatch")
class RecentlyPlayedView(SpotifyAPIView):
    spotify_endpoint = "https://api.spotify.com/v1/me/player/recently-played"

    def handle_response(self, response, time_frame):
        recently_played_data = response.json().get("items", [])
        tracks = []

        for _, track_data in enumerate(recently_played_data):
            track, _ = Track.objects.update_or_create(
                song_id=track_data["track"]["id"],
                defaults={
                    "name": track_data["track"]["name"],
                    "img_url": track_data["track"]["album"]["images"][0]["url"],
                },
            )

            for artist_data in track_data["track"]["artists"]:
                artist, _ = Artist.objects.update_or_create(
                    artist_id=artist_data["id"],
                    defaults={
                        "name": artist_data["name"],
                    },
                )
                track.artists.add(artist)

            tracks.append(track)

        Track.objects.bulk_create(tracks, ignore_conflicts=True)

        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)
