from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import CustomUser
from apps.spotify.models import Artist, Track, UserTrackRelation
from apps.spotify.serializers import TrackSerializer
from apps.spotify.util import make_spotify_api_request


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def top_tracks_view(request, user_id):
    user = get_object_or_404(CustomUser, spotify_user_id=user_id)
    spotify_endpoint = "https://api.spotify.com/v1/me/top/tracks"
    params = {"limit": request.query_params.get("limit", 20)}
    response = make_spotify_api_request(user.spotify_user_id, spotify_endpoint, params)

    if response.status_code == 200:
        spotify_data = response.json()
        tracks_data = process_spotify_tracks_data(user, spotify_data["items"])
        return Response({"items": tracks_data})
    else:
        return Response({"error": "Failed to retrieve top tracks from Spotify"}, status=response.status_code)


def process_spotify_tracks_data(user, spotify_tracks):
    processed_tracks = []
    last_relations = UserTrackRelation.objects.filter(user=user).order_by("position")

    for index, spotify_track in enumerate(spotify_tracks, start=1):
        track, _ = Track.objects.get_or_create(
            spotify_id=spotify_track["id"],
            defaults={
                "name": spotify_track["name"],
                "img_url": spotify_track["album"]["images"][0]["url"] if spotify_track["album"]["images"] else None,
                "duration_ms": spotify_track["duration_ms"],
                "spotify_popularity": spotify_track["popularity"],
                "spotify_preview_url": spotify_track["preview_url"],
                "explicit": spotify_track["explicit"],
            },
        )
        for spotify_artist in spotify_track["artists"]:
            artist, _ = Artist.objects.get_or_create(
                spotify_id=spotify_artist["id"], defaults={"name": spotify_artist["name"]}
            )
            track.artists.add(artist)

        indicator = "NEW"
        for relation in last_relations:
            if relation.track == track:
                if relation.position > index:
                    indicator = "UP"
                elif relation.position < index:
                    indicator = "DOWN"
                else:
                    indicator = "STABLE"
                break

        track_data = TrackSerializer(track).data
        track_data["position"] = index
        track_data["indicator"] = indicator

        processed_tracks.append(track_data)

        UserTrackRelation.objects.update_or_create(
            user=user, track=track, defaults={"position": index, "indicator": indicator}
        )

    return processed_tracks
