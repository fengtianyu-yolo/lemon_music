from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from django.views import View
from enum import Enum
from ..models import SongModel, ArtistModel, Song2ArtistModel
import os
import mutagen

# Create your views here.

class Search(View):
    
    def get(self, request):                    
        name = request.GET.get('name')
        if name != None:
            songs = SongModel.objects.filter(song_name=name)
            result = []
            for song in songs:
                result.append(song.song_name)
            return JsonResponse({'code': 200, 'songs': result})
        
        # 联表查询，找歌手为xx的所有歌曲
        artist = request.GET.get('artist')
        if artist != None:
            artists = ArtistModel.objects.filter(artist_name__contains=artist)
            if artists != None and len(artists) > 0:
                models = Song2ArtistModel.objects.filter(artist=artists[0])
                result = []
                for model in models:
                    result.append(model.song.song_name)
                return JsonResponse({'code': 200, 'list': result})
            return JsonResponse({'code': 200, 'list': ''})
        return JsonResponse({'code': 200, 'list': ''})



class SearchArtist(View):
    def get(self, request):
        name = request.GET.get('name')
        if name != None:
            artists = ArtistModel.objects.filter(artist_name__contains=name)
            result = []
            for artist in artists:
                result.append(artist.artist_name)
            return JsonResponse({'code': 200, 'list': result})
        else:
            return JsonResponse('')
        