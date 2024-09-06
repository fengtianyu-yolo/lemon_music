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

class RefreshList(View):
    root_path = '/Volumes/MdieaLib/音乐库'

    def get(self, request):        
        # 遍历根目录 
        file_list = self.travel(self.root_path)
        # 解析文件 
        # 生成Model 
        # 生成Artist 
        return JsonResponse({'code': 200, 'files': file_list})
        
    def travel(self, path) -> list[str]:
        result = []
        sub_itmes = os.listdir(path)
        for item in sub_itmes:
            full_path = path + '/' + item
            name = self.retrive_song_info(full_path, item)
            result.append(name)
        
    def retrive_song_info(self, file_path, file_name) -> str:
        
        song = mutagen.File(file_path)

        # 去重检查 
        if self.exist(file_name):
            print('数据库中已经存在,' + file_name)
            return ''

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
            # print('名字 = ' + str(song_name))
            # print('歌手 = ' + str(artist_name))
            
        elif file_type == 'audio/mp3':            
            song_name = song.tags['TIT2']
            artist_name = song.tags['TPE1']
            songModel.song_name = song_name
            songModel.media_type = MediaType.MP3.value 
            songModel.hq_file_path = file_path 
            songModel.hq_file_name = file_name
            artist.artist_name = artist_name
            # print('file is mp3')
            # print('名字 = ' + str(song_name))
            # print('歌手 = ' + str(artist_name))

        else:
            print('处理失败: ' + file_name)
            return ''

        duration = song.info.length
        songModel.duration = duration
        
        song_artist.song = songModel 
        song_artist.artist = artist

        songModel.save() 
        artist.save() 
        song_artist.save() 
        return file_name
        # print('时长 = ' + str(duration))

    def exist(self, file_name) -> bool: 
        SongModel.objects.filter(sq_file_name=file_name)
        return False