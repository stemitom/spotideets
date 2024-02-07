from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.spotify.util import make_spotify_api_request

User = get_user_model()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def top_artists(request, user_id):
    spotify_endpoint = "https://api.spotify.com/v1/me/top/artists"
    time_range = request.query_params.get("time_range", "medium_term")  # Default to 'medium_term'
    limit = request.query_params.get("limit", 20)
    params = {"time_range": time_range, "limit": limit}

    response = make_spotify_api_request(user_id, spotify_endpoint, params)
    if response.status_code == 200:
        spotify_data = response.json()
        processed_data = process_spotify_artists_data(spotify_data)
        return Response({"items": processed_data})
    else:
        return Response({"error": "Failed to retrieve top artists from Spotify"}, status=response.status_code)


def process_spotify_artists_data(spotify_data):
    items = spotify_data.get("items", [])
    processed_items = []
    for index, item in enumerate(items, start=1):
        processed_item = {
            "position": index,
            "streams": None,  # Spotify doesn't provide stream counts in this endpoint
            "indicator": "NEW",  # Logic to determine this would go here
            "artist": {
                "externalIds": {"spotify": [item.get("id")]},
                "followers": item.get("followers", {}).get("total"),
                "genres": item.get("genres", []),
                "id": item.get("id"),  # Assuming this is a unique ID you assign, not Spotify's
                "image": item.get("images", [{}])[0].get("url"),  # Taking the first image
                "name": item.get("name"),
                "spotifyPopularity": item.get("popularity"),
            },
        }
        processed_items.append(processed_item)
    return processed_items
