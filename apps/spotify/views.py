import pprint

import requests
from decouple import config
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView

from apps.spotify.util import (create_or_update_spotify_user,
                               get_spotify_user_data)


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
        print(token_data["access_token"])

        if "access_token" not in token_data:
            return HttpResponseBadRequest("Access token not received")

        spotify_user = create_or_update_spotify_user(token_data)
        authenticated_user = authenticate(
            request,
            spotify_user_email=spotify_user.spotify_user_email,
            spotify_user_id=spotify_user.spotify_user_id,
        )
        login(request, authenticated_user)
        print('logged in')

        return HttpResponseRedirect(reverse("spotify:success"))


def oauth_logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("spotify:oauth"))


def oauth_success_view(request):
    return render(request, "oauth-success.html")


def oauth_index_view(request):
    return render(request, "oauth-home.html")
