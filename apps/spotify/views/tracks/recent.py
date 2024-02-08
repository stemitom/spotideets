from typing import List, Dict, Any
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.accounts.models import CustomUser
from apps.spotify.decorators import check_privacy_settings
from apps.spotify.models import Artist, Track
from apps.spotify.serializers import TrackSerializer
from apps.spotify.util import make_spotify_api_request


@api_view(["GET"])
@check_privacy_settings("show_recently_played")
def recently_played_view(request, user_id: str) -> Response:
    user = get_object_or_404(CustomUser, spotify_user_id=user_id)
    spotify_endpoint = "https://api.spotify.com/v1/me/player/recently-played"
    params = {"limit": request.query_params.get("limit", 20)}
    response = make_spotify_api_request(user.spotify_user_id, spotify_endpoint, params)

    if response.status_code == 200:
        spotify_data = response.json()
        tracks_data = process_recently_played_data(spotify_data["items"])
        return Response({"items": tracks_data})
    else:
        return Response(
            {"error": "Failed to retrieve recently played tracks from Spotify"}, status=response.status_code
        )


def process_recently_played_data(spotify_tracks: List[Dict[str, Any]]) -> List:
    processed_tracks = []
    for item in spotify_tracks:
        spotify_track = item["track"]
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

        track_data = TrackSerializer(track).data
        processed_tracks.append(track_data)

    return processed_tracks
