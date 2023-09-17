import pprint
import requests
from decouple import config
from django.contrib.auth import logout
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView

from apps.spotify.util import create_or_update_spotify_user


class SpotifyOauthView(APIView):
    def get(self, request):
        spotify_auth_url = "https://accounts.spotify.com/authorize"
        scopes = config("SPOTIFY_PERMISSION_SCOPES")
        spotify_auth_url = (
            requests.Request(
                "GET",
                spotify_auth_url,
                params={
                    "scope": scopes,
                    "response_type": "code",
                    "redirect_uri": config("SPOTIFY_REDIRECT_URI"),
                    "client_id": config("SPOTIFY_CLIENT_ID"),
                },
            )
            .prepare()
            .url
        )

        return redirect(spotify_auth_url)


class SpotifyOAuthCallbackView(View):
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return HttpResponseBadRequest("Authorization code missing")

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config("SPOTIFY_REDIRECT_URI"),
            "client_id": config("SPOTIFY_CLIENT_ID"),
            "client_secret": config("SPOTIFY_CLIENT_SECRET"),
        }

        response = requests.post("https://accounts.spotify.com/api/token", data=data)
        token_data = response.json()
        pprint.pprint(token_data)

        if "access_token" not in token_data:
            return HttpResponseBadRequest("Access token not received")

        user = create_or_update_spotify_user(token_data)
        pprint.pprint(user)

        return HttpResponseRedirect(reverse("spotify:success"))


def oauth_logout_view(request):
    logout(request)
    print("log-out")
    return redirect("spotify:oauth")


def oauth_success_view(request):
    return render(request, "oauth-success.html")


def oauth_index_view(request):
    return render(request, "oauth-home.html")
