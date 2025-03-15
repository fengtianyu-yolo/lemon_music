from rest_framework import serializers
from .models import Song, File, Artist, Tag 

class SongSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True)
    tags = TagSerializer(many=True)
    File = FileSerializer(many=True)
    class Meta:
        model = Song
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'