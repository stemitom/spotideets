from enumfields.drf import EnumSupportSerializerMixin

from rest_framework import serializers

from apps.spotify.models import Album, Artist, Genre, TopArtists, TopGenres, TopTracks, Track


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id", "name"]


class TopArtistsSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    artist = ArtistSerializer()

    class Meta:
        model = TopArtists
        fields = ["position", "streams", "indicator", "artist"]


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ["id", "name", "image"]


class TrackSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True)
    albums = AlbumSerializer(many=True)

    class Meta:
        model = Track
        fields = [
            "id",
            "name",
            "artists",
            "albums",
            "duration_ms",
            "explicit",
            "spotify_popularity",
            "spotify_preview",
        ]


class TopTracksSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    track = TrackSerializer()

    class Meta:
        model = TopTracks
        fields = ["position", "streams", "indicator", "track"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class TopGenresSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = TopGenres
        fields = ["position", "streams", "indicator", "genre"]
