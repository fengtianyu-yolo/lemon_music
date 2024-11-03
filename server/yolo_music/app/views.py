from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from django.views import View
from enum import Enum
from .models import SongModel, ArtistModel, Song2ArtistModel
import os
import mutagen
from .Utils import Utils, ColorLabel

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
        # 遍历根目录 - 筛选目标文件 - 去重 - 存入数据库 
        file_list = self.travel(self.root_path)
        # 解析文件 
        # 生成Model 
        # 生成Artist 
        return JsonResponse({'code': 200, 'files': file_list})
        
    def travel(self, path) -> list[str]:
        result = []
        sub_itmes = os.listdir(path)
        files = list(filter(lambda x: not x.startswith('.') and not x.endswith('lrc') , sub_itmes))
        
        for item in files:                        
            full_path = path + '/' + item
            name = self.retrive_song_info(full_path, item)
            
            if not name is None and len(name) > 0:
                result.append(name)
        
        print('处理文件数量: ' + str(len(result)))
        return result 
        

    def retrive_song_info(self, file_path, file_name) -> str:

        # 去重检查 
        if self.exist(filename=file_name, filepath=file_path):
            print('数据库中已经存在,' + file_name)
            return 

        checkResult = self.valid(file_path)
        status = checkResult[0]
        song = checkResult[1]
        
        if status == False:
            return 

        if song == None:
            Utils.set_label(file_path, ColorLabel.gray.value)
            print('处理失败: ' + file_name)
            return

        songModel = SongModel() 
        # artistModel = ArtistModel()
        artistList: list[ArtistModel] = []
        file_type = song.mime[0] 
        
        success = False
        if file_type == 'audio/flac':
            success = self.retrive_flac(song=song, artists=artistList, songModel=songModel, file_name=file_name, file_path=file_path)
            
        elif file_type == 'audio/mp3':            
            success = self.retrive_mp3(song=song, songModel=songModel, artists=artistList, filename=file_name, filepath=file_path)

        else:
            print('处理失败: ' + file_name)
            Utils.set_label(file_path, ColorLabel.gray.value)
            return ''

        if success == False:
            return ''

        duration = song.info.length
        songModel.duration = duration
        songModel.save() 

        for artist in artistList:
            songArtistModel = Song2ArtistModel() 
            songArtistModel.song = songModel 
            songArtistModel.artist = artist            
            artist.save() 
            songArtistModel.save() 
        Utils.set_label(file_path, ColorLabel.green.value)
        return file_name


    def valid(self, file_path) -> tuple:
        try:
            song = mutagen.File(file_path)
        except:
            print('文件无法解析: ' + file_path)
            return (False, None)
        else:
            return (True, song)


    def retrive_flac(self, song, artists: list[ArtistModel], songModel: SongModel, file_name: str, file_path: str) -> bool:
        try:
            song_name = song.tags['TITLE']
            artist_name = song.tags['ARTIST']            
        except:
            print('FLAC处理失败: ' + file_name)
            Utils.set_label(file_path, ColorLabel.gray.value)
            return False
        else:
            songModel.media_type = 1
            songModel.song_name = song_name
            songModel.media_type = MediaType.FLAC.value
            songModel.sq_file_path = file_path 
            songModel.sq_file_name = file_name
            self.retrive_artist(artists, artist_name)
            return True
  
    def retrive_mp3(self, song, songModel: SongModel, artists: list[ArtistModel], filename: str, filepath: str) -> bool:
        try:
            song_name = song.tags['TIT2']
            artist_name = song.tags['TPE1']
        except:
            print('MP3处理失败: ' + filename)
            Utils.set_label(filepath, ColorLabel.gray.value)
            return False
        else:
            songModel.song_name = song_name
            songModel.media_type = MediaType.MP3.value 
            songModel.hq_file_path = filepath 
            songModel.hq_file_name = filename
            self.retrive_artist(artists, artist_name)
            return True

      
    def retrive_artist(self, artistList: list[ArtistModel], name):
            if '、' in name:
                nameList = name.split('、')
                for artistName in nameList:
                    existArtist = self.findArtist(artist_name=artistName)
                    if existArtist:
                        artistList.append(artist)
                    else:
                        artist = ArtistModel()
                        artist.artist_name = artistName          
                        artistList.append(artist)
            else:
                existArtist = self.findArtist(artist_name=artistName)
                if existArtist:
                    artistList.append(artist)
                else:
                    artist = ArtistModel()
                    artist.artist_name = artistName          
                    artistList.append(artist)
                

    def findArtist(self, artist_name):
        artist = ArtistModel.objects.filter(artist_name=artist_name)
        if artist.count > 0:
            return artist[0]
        else:
            return None

    def exist(self, filepath, filename) -> bool: 
        if len(SongModel.objects.filter(sq_file_name=filename)) > 0:
            return True
        elif len(SongModel.objects.filter(hq_file_name=filename)) > 0:
            return True
        else:
            return False
        
        # color = Utils.get_file_label(filepath=filepath)
        if color == ColorLabel.green:
            return True
        else:
            return False
        

"""
TODO:  
- 完成列表接口
- 处理wav文件 
- 处理ape文件 
- 将全量扫描改为增量扫描
"""