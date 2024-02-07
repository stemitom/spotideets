from django.urls import path

from apps.spotify.views.tracks.top import top_tracks_view
from apps.spotify.views.tracks.recent import recently_played_view

from .views.auth import SpotifyOAuthCallbackView, SpotifyOAuthView, oauth_logout_view, oauth_success_view
# from .views.tracks import RecentlyPlayedView, TopTracksView

app_name = "spotify"

urlpatterns = [
    path(
        "oauth",
        SpotifyOAuthView.as_view(),
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
        "signout",
        oauth_logout_view,
        name="signout",
    ),
    path(
        "users/<str:user_id>/top/tracks",
        top_tracks_view,
        name="top-track",
    ),
    # path(
    #     "users/<str:user_id>/top/artists",
    #     top_artists,
    #     name="top-artists",
    # ),
    path(
        "users/<str:user_id>/streams/recent",
        recently_played_view,
        name="recently-played",
    ),
]
