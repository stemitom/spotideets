from datetime import timezone

from django.conf import settings
from django.db import models


class SpotifyToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=1000)
    refresh_token = models.CharField(max_length=1000)
    token_type = models.CharField(max_length=100)
    expires_in = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_token_expired(self):
        return timezone.now() > (
            self.created_at + timezone.timedelta(seconds=self.expires_in)
        )
