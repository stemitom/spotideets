from rest_framework import serializers

from .models import CustomUser, PrivacySettings


class CustomUserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "spotify_user_email", "spotify_user_id", "bio", "display_name", "custom_url")
        read_only_fields = ['custom_url', 'spotify_user_email', 'spotify_user_id']


class PrivacySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacySettings
        fields = '__all__'