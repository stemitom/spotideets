from rest_framework import serializers

from .models import Track


class TrackSerializer(serializers.ModelSerializer):
    artist_names = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = ["song_id", "artist_names", "name", "img_url"]

    def get_artist_names(self, obj):
        return ", ".join([artist.name for artist in obj.artists.all()])
