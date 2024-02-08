from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.accounts.models import CustomUser
from apps.spotify.decorators import check_privacy_settings
from apps.spotify.models import Artist, Genre, UserArtistRelation
from apps.spotify.serializers import ArtistSerializer
from apps.spotify.util import make_spotify_api_request

User = get_user_model()


@api_view(["GET"])
@check_privacy_settings("show_top_artists")
def top_artists_view(request, user_id: str) -> Response:
    user = get_object_or_404(CustomUser, spotify_user_id=user_id)
    spotify_endpoint = "https://api.spotify.com/v1/me/top/artists"
    time_range = request.query_params.get("time_range", "medium_term")
    limit = request.query_params.get("limit", 20)
    params = {"time_range": time_range, "limit": limit}
    response = make_spotify_api_request(user.spotify_user_id, spotify_endpoint, params)

    if response.status_code == 200:
        spotify_data = response.json()
        processed_data = process_spotify_artists_data(user, spotify_data["items"])
        return Response({"items": processed_data})
    else:
        return Response({"error": "Failed to retrieve top artists from Spotify"}, status=response.status_code)


def process_spotify_artists_data(user, spotify_artists):
    processed_artists = []
    last_relations = {relation.artist.spotify_id: relation for relation in UserArtistRelation.objects.filter(user=user)}

    for index, item in enumerate(spotify_artists, start=1):
        artist, created = Artist.objects.get_or_create(
            spotify_id=item["id"],
            defaults={
                "name": item["name"],
                "img_url": item["images"][0]["url"] if item["images"] else None,
                "spotify_popularity": item["popularity"],
                "followers_count": item["followers"]["total"],
            },
        )

        if created:
            for genre_name in item["genres"]:
                genre, _ = Genre.objects.get_or_create(name=genre_name)
                artist.genres.add(genre)
        else:
            artist.genres.clear()
            for genre_name in item["genres"]:
                genre, _ = Genre.objects.get_or_create(name=genre_name)
                artist.genres.add(genre)

        relation = last_relations.pop(artist.spotify_id, None)
        if relation:
            if relation.position < index:
                indicator = "DOWN"
            elif relation.position > index:
                indicator = "UP"
            else:
                indicator = "STABLE"
        else:
            indicator = "NEW"

        UserArtistRelation.objects.update_or_create(
            user=user, artist=artist, defaults={"position": index, "indicator": indicator}
        )

        artist_data = ArtistSerializer(artist).data
        artist_data["position"] = index
        artist_data["indicator"] = indicator
        processed_artists.append(artist_data)

    return processed_artists
