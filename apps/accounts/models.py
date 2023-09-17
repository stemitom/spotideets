from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    spotify_user_email = models.EmailField(unique=True)
    spotify_user_id = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.spotify_user_id}"