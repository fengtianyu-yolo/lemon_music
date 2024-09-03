from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from django.views import View
from .models import SongModel
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
            self.retrive_song_info(full_path)
        
    def retrive_song_info(self, file_path):
        songModel = SongModel() 
        
        song = mutagen.File(file_path)
        file_type = song.mime[0] 
        if file_type == 'audio/ape':
            print('file is ape')
            song_name = song.tags['title']
            print('名字 = ' + str(song_name))
        
        elif file_type == 'audio/flac':
            song_name = song.tags['TITLE']
            artist_name = song.tags['ARTIST']
            print('名字 = ' + str(song_name))
            print('歌手 = ' + str(artist_name))
            songModel.media_type = 1
            songModel.song_name = song_name
            
        elif file_type == 'audio/mp3':
            print('file is mp3')
            song_name = song.tags['TIT2']
            artist_name = song.tags['TPE1']
            print('名字 = ' + str(song_name))
            print('歌手 = ' + str(artist_name))
        
        else:
            print('解析失败')

        duration = song.info.length
        songModel.duration = duration
        print('时长 = ' + str(duration))

    