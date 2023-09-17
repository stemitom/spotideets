import requests
from decouple import config
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView


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


class SpotifyOAuthCallback(View):
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

        if "access_token" not in token_data:
            return HttpResponseBadRequest("Access token not received")

        access_token = token_data["access_token"]
        print(access_token)

        return HttpResponseRedirect(reverse("spotify:oauth-success"))


def oauth_success(request):
    return render(request, "oauth-success.html")


def oauth_index(request):
    return render(request, "oauth-home.html")
