from django.urls import path

from .views import (
    SpotifyOAuthCallbackView,
    SpotifyOauthView,
    oauth_logout_view,
    oauth_success_view,
)

app_name = "spotify"

urlpatterns = [
    path(
        "oauth",
        SpotifyOauthView.as_view(),
        name="oauth",
    ),
    path(
        "callback",
        SpotifyOAuthCallbackView.as_view(),
        name="callback",
    ),
    path(
        "success",
        oauth_success_view,
        name="success",
    ),
    path(
        "logout",
        oauth_logout_view,
        name="logout",
    ),
]
