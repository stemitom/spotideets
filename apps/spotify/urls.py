from django.urls import path

from apps.spotify.views.artists import TopArtistsView

from .views.auth import SpotifyOAuthCallbackView, SpotifyOAuthView, oauth_logout_view, oauth_success_view
from .views.tracks import RecentlyPlayedView, TopTracksView

app_name = "spotify"

urlpatterns = [
    path(
        "oauth/",
        SpotifyOAuthView.as_view(),
        name="oauth",
    ),
    path(
        "callback/",
        SpotifyOAuthCallbackView.as_view(),
        name="callback",
    ),
    path(
        "success/",
        oauth_success_view,
        name="success",
    ),
    path(
        "signout/",
        oauth_logout_view,
        name="signout",
    ),
    path(
        "users/<str:user_id>/top/tracks/",
        TopTracksView.as_view(),
        name="top-track",
    ),
    path(
        "users/<str:user_id>/top/artists/",
        TopArtistsView.as_view(),
        name="top-artists",
    ),
    path(
        "users/<str:user_id>/streams/recent/",
        RecentlyPlayedView.as_view(),
        name="recently-played",
    ),
]
