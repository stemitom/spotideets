from django.contrib.auth.backends import ModelBackend

from apps.accounts.models import CustomUser


class SpotifyAuthBackend(ModelBackend):
    def authenticate(self, request, spotify_user_email=None, spotify_user_id=None):
        try:
            user = CustomUser.objects.get(
                spotify_user_email=spotify_user_email, spotify_user_id=spotify_user_id
            )
            return user
        except CustomUser.DoesNotExist:
            return None
