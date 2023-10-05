from collections import defaultdict

import requests

from django.utils import timezone

from apps.accounts.models import CustomUser
from apps.spotify.models import SpotifyToken
from commons.enums import IndicatorEnum


def get_spotify_user_data(access_token):
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except TimeoutError:
        return ""

    if response.status_code == 200:
        data = response.json()
        return data
    return None


def get_artist_genres(artist_id, access_token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    genres = data.get("genres", [])
    return genres


def create_or_update_spotify_user(token_data):
    user_data = get_spotify_user_data(token_data["access_token"])

    user, _ = CustomUser.objects.get_or_create(
        spotify_user_email=user_data["email"],
        spotify_user_id=user_data["id"],
    )

    try:
        spotify_token = user.spotifytoken
    except SpotifyToken.DoesNotExist:
        spotify_token = SpotifyToken(user=user)

    spotify_token.access_token = token_data["access_token"]
    spotify_token.refresh_token = token_data["refresh_token"]
    spotify_token.token_type = token_data["token_type"]
    spotify_token.expires_in = token_data["expires_in"]

    if not spotify_token.created_at:
        spotify_token.created_at = timezone.now()
    spotify_token.save()

    return user


def calculate_indicator(current_positions):
    """
    Calculate the indicator based on the current positions and their previous positions.

    Args:
        current_positions (list): A list of current positions of the resources.

    Returns:
        dict: A dictionary containing resource_id as keys and their indicators ('up', 'down', 'same') as values.
    """
    indicators = defaultdict(lambda: "same")
    previous_positions = defaultdict(lambda: None)

    for position, resource_id in enumerate(current_positions, start=1):
        previous_position = previous_positions[resource_id]
        if previous_position is not None:
            if position < previous_position:
                indicators[resource_id] = IndicatorEnum.UP
            elif position > previous_position:
                indicators[resource_id] = IndicatorEnum.DOWN
        previous_positions[resource_id] = position

    return dict(indicators)
