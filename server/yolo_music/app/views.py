from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from django.views import View
from enum import Enum
from .models import SongModel, ArtistModel, Song2ArtistModel
import os
import mutagen
# Create your views here.

def test(request):
    return HttpResponse('Hello World')

class TestView(View):
    def get(self, request):
        return HttpResponse('ok')
    
class Test2View(View):
    def get(self, request):
        msg = request.GET.get('msg')
        return JsonResponse({'code': 200, 'data': msg})
    
class Test4View(View):
    def get(self, request, msg, id):        
        return JsonResponse({'code': 200, 'data': msg, 'id': id})    
    

class MediaType(Enum):
    FLAC = 1
    MP3 = 2 
    WAV = 3 

class RefreshList(View):
    def get(self, request):
        root_path = '' 
        # 遍历根目录 
        self.travel(root_path)
        # 解析文件 
        # 生成Model 
        # 生成Artist 
        return JsonResponse({'code': 200})
        
    def travel(self, path):
        sub_itmes = os.listdir(path)
        for item in sub_itmes:
            full_path = path + '/' + item
            self.retrive_song_info(full_path, item)
        
    def retrive_song_info(self, file_path, file_name):
        
        song = mutagen.File(file_path)

        # 去重检查 
        if self.exist():
            return

        songModel = SongModel() 
        artist = ArtistModel()
        song_artist = Song2ArtistModel() 
        file_type = song.mime[0] 
        
        if file_type == 'audio/flac':
            song_name = song.tags['TITLE']
            artist_name = song.tags['ARTIST']            
            songModel.media_type = 1
            songModel.song_name = song_name
            songModel.media_type = MediaType.FLAC.value
            songModel.sq_file_path = file_path 
            songModel.sq_file_name = file_name
            artist.artist_name = artist_name            
            print('名字 = ' + str(song_name))
            print('歌手 = ' + str(artist_name))
            
        elif file_type == 'audio/mp3':            
            song_name = song.tags['TIT2']
            artist_name = song.tags['TPE1']
            songModel.song_name = song_name
            songModel.media_type = MediaType.MP3.value 
            songModel.hq_file_path = file_path 
            songModel.hq_file_name = file_name
            artist.artist_name = artist_name
            print('file is mp3')
            print('名字 = ' + str(song_name))
            print('歌手 = ' + str(artist_name))
        
        else:
            print('解析失败: ' + file_name)
            return

        duration = song.info.length
        songModel.duration = duration
        
        song_artist.song = songModel 
        song_artist.artist = artist

        songModel.save() 
        artist.save() 
        song_artist.save() 
        print('时长 = ' + str(duration))

    def exist(self) -> bool: 
        return False