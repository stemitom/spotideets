from datetime import timedelta

import requests
from decouple import config
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from apps.spotify.models import SpotifyToken


class SpotifyTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, "user") and request.user.is_authenticated:
            user = request.user
            try:
                spotify_token = user.spotifytoken
            except SpotifyToken.DoesNotExist:
                spotify_token = None

            if spotify_token and not spotify_token.access_token:
                return self.redirect_to_spotify_auth(request)

            if spotify_token and spotify_token.is_token_expired():
                refresh_success = self.refresh_spotify_token(user)
                if not refresh_success:
                    return self.redirect_to_spotify_auth(request)

        response = self.get_response(request)
        return response

    def redirect_to_spotify_auth(self, request):
        return HttpResponseRedirect(reverse("spotify:oauth"))

    def refresh_spotify_token(self, user):
        if not user:
            return False

        try:
            spotify_token = user.spotifytoken
        except SpotifyToken.DoesNotExist:
            return False

        if not spotify_token.refresh_token:
            return False

        data = {
            "grant_type": "refresh_token",
            "refresh_token": spotify_token.refresh_token,
            "client_id": config("SPOTIFY_CLIENT_ID"),
            "client_secret": config("SPOTIFY_CLIENT_SECRET"),
        }

        response = requests.post("https://accounts.spotify.com/api/token", data=data)

        if response.status_code == 200:
            token_data = response.json()
            spotify_token.access_token = token_data["access_token"]
            spotify_token.expires_at = timezone.now() + timedelta(
                seconds=token_data["expires_in"]
            )
            spotify_token.save()
            return True

        return False
