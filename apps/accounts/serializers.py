from rest_framework import serializers

from .models import CustomUser, PrivacySettings


class PrivacySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacySettings
        exclude = ("user", "id")


class CustomUserRetrieveUpdateSerializer(serializers.ModelSerializer):
    privacy_settings = PrivacySettingsSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "spotify_user_email",
            "spotify_user_id",
            "bio",
            "display_name",
            "custom_url",
            "privacy_settings",
        )

        read_only_fields = ["custom_url", "spotify_user_email", "spotify_user_id", "privacy_settings"]
