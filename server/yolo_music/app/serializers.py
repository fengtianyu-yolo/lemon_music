from rest_framework import serializers
from .models import Song, Artist, File

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_path', 'format_type']

class SongSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)
    
    class Meta:
        model = Song
        fields = ['id', 'title', 'duration', 'cover', 'artists', 'files', 'play_count']