from django.contrib import admin
from django.urls import include, path

from apps.spotify.views import oauth_index_view

urlpatterns = [
    path(
        "",
        oauth_index_view,
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
