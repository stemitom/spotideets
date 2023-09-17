from django.urls import path
from .views import SpotifyOauthView, SpotifyOAuthCallback, oauth_success

app_name = "spotify"

urlpatterns = [
    path("oauth", SpotifyOauthView.as_view(), name="oauth"),
    path("callback", SpotifyOAuthCallback.as_view(), name="callback"),
    path("success", oauth_success, name="oauth-success"),
]
