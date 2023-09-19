from django.conf import settings
from django.db import models
from django.utils import timezone


class SpotifyToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=1000)
    refresh_token = models.CharField(max_length=1000)
    token_type = models.CharField(max_length=100)
    expires_in = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

    def is_token_expired(self):
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        self.expires_at = self.update_at + timezone.timedelta(
            seconds=self.expires_in,
        )
        super().save(*args, **kwargs)
