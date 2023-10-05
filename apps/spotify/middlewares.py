from datetime import timedelta

import requests
from decouple import config
from requests.exceptions import Timeout

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import resolve, reverse
from django.utils import timezone

from apps.accounts.models import PrivacySettings
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

        try:
            response = requests.post("https://accounts.spotify.com/api/token", data=data, timeout=5)
        except Timeout:
            return False

        if response.status_code == 200:
            token_data = response.json()
            spotify_token.access_token = token_data["access_token"]
            spotify_token.expires_at = timezone.now() + timedelta(seconds=token_data["expires_in"])
            spotify_token.save()
            return True

        return False


class PrivacyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = resolve(request.path_info).kwargs.get('user_id')

        endpoint_privacy_settings = {
            'top_tracks': 'show_top_tracks',
            'top_genres': 'show_top_genres',
            'top_artists': 'show_top_artists',
        }

        endpoint_name = request.path_info.split('/')[-2]
        privacy_setting = endpoint_privacy_settings.get(endpoint_name)

        if privacy_setting:
            if request.user.is_authenticated and request.user.id != user_id:
                privacy_settings = PrivacySettings.objects.get(user_id=user_id)
                if not getattr(privacy_settings, privacy_setting):
                    raise PermissionDenied(f"Access to {privacy_setting} is denied due to privacy settings.")

        response = self.get_response(request)
        return response
