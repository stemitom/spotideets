from django.contrib import admin
from django.urls import path, include

from apps.spotify.views import oauth_index


urlpatterns = [
    path(
        "",
        oauth_index,
        name="spotify-oauth",
    ),
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "spotify/",
        include("apps.spotify.urls"),
    ),
]
