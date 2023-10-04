import requests
from decouple import config

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from rest_framework.views import APIView

from apps.spotify.util import create_or_update_spotify_user


class SpotifyOAuthView(APIView):
    """
    View for initiating the Spotify OAuth flow.
    """

    def get(self, request):
        spotify_auth_url = "https://accounts.spotify.com/authorize"
        scopes = config("SPOTIFY_PERMISSION_SCOPES")
        params = {
            "scope": scopes,
            "response_type": "code",
            "redirect_uri": config("SPOTIFY_REDIRECT_URI"),
            "client_id": config("SPOTIFY_CLIENT_ID"),
            "show_dialog": False,
        }

        if not request.user.is_authenticated:
            params["show_dialog"] = True

        spotify_auth_url = (
            requests.Request(
                "GET",
                spotify_auth_url,
                params=params,
            )
            .prepare()
            .url
        )

        return redirect(spotify_auth_url)


class SpotifyOAuthCallbackView(View):
    """
    View for handling the callback after Spotify OAuth authentication.
    """

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

        try:
            spotify_user = create_or_update_spotify_user(token_data)
            authenticated_user = authenticate(
                request,
                spotify_user_email=spotify_user.spotify_user_email,
                spotify_user_id=spotify_user.spotify_user_id,
            )
            if authenticated_user is not None:
                login(request, authenticated_user)
                return HttpResponseRedirect(reverse_lazy("spotify:success"))
            else:
                return HttpResponseBadRequest("Failed to authenticate user")
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")


@login_required
def oauth_logout_view(request):
    """
    View for logging out the user.
    """
    logout(request)
    return HttpResponseRedirect(reverse_lazy("index"))


def oauth_success_view(request):
    """
    View for displaying the success page after
    """
    return render(request, "oauth-success.html")


def oauth_index_view(request):
    """
    View for displaying the home page for Spotify OAuth authentication.
    """
    return render(request, "oauth-home.html")
