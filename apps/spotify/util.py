from typing import Any, Dict, List, Optional

import requests
from django.utils import timezone

from apps.accounts.models import CustomUser
from apps.spotify.models import SpotifyToken


def get_spotify_user_data(access_token: str) -> Optional[Dict[str, Any]]:
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

    if response.status_code == 200:
        data = response.json()
        return data
    return None


def get_artist_genres(artist_id: str, access_token: str) -> Optional[List[str]]:
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

    if response.status_code == 200:
        data = response.json()
        genres = data.get("genres", [])
        return genres

    print(f"Request failed with status code {response.status_code}")
    return None


def create_or_update_spotify_user(token_data):
    user_data = get_spotify_user_data(token_data.get("access_token", ""))
    if not user_data:
        return None

    user, _ = CustomUser.objects.get_or_create(
        spotify_user_email=user_data.get("email"),
        spotify_user_id=user_data.get("id"),
        defaults={"username": user_data.get("id")},
    )

    try:
        spotify_token = user.spotifytoken
    except SpotifyToken.DoesNotExist:
        spotify_token = SpotifyToken(user=user)

    spotify_token.access_token = token_data.get("access_token")
    spotify_token.refresh_token = token_data.get("refresh_token")
    spotify_token.token_type = token_data.get("token_type")
    spotify_token.expires_in = token_data.get("expires_in")

    if not spotify_token.created_at:
        spotify_token.created_at = timezone.now()
    spotify_token.save()

    return user
