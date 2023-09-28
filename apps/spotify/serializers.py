from rest_framework import serializers

from apps.spotify.models import Artist, Genre, Track


class TrackSerializer(serializers.ModelSerializer):
    artist_names = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = ["song_id", "artist_names", "name", "img_url"]

    def get_artist_names(self, obj):
        return ", ".join([artist.name for artist in obj.artists.all()])


class ArtistSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Artist
        fields = ["artist_id", "name", "genres"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"
