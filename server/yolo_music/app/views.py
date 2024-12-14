from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from django.views import View
from enum import Enum

import mutagen.id3
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
        """
            遍历文件夹
        """
        result = []
        sub_itmes = os.listdir(path)
        files = list(filter(lambda x: not x.startswith('.') and not x.endswith('lrc') , sub_itmes))
        
        for item in files:                        
            full_path = path + '/' + item
            print(f"开始处理文件：{item} ... ")
            name = self.storeSong(full_path, item)
            
            if not name is None and len(name) > 0:
                result.append(name)
                print()
            else:
                print(f"{item} 文件处理失败 ❓ \n")
        
        print('处理文件数量: ' + str(len(result)))
        return result 
        

    def storeSong(self, file_path, file_name) -> str:
        """
        处理歌曲文件，如果该首歌曲已经存在，为音乐增加无损音乐；如果歌曲不存在，创建歌曲信息保存到数据库
        """
        # 检查文件是否已经处理过了检查 ：增量更新和存量更新的区别
        if self.exist(filename=file_name, filepath=file_path):
            print('数据库中已经存在,' + file_name)
            return 

        # 文件是否可以被处理
        checkResult = self.valid(file_path)
        status = checkResult[0]
        song = checkResult[1]        
        if status == False or song == None:
            Utils.set_label(file_path, ColorLabel.gray.value)
            print('处理失败: ' + file_name)
            return
        
        file_type = song.mime[0] 
        songModel = SongModel()
        artistList: list[ArtistModel] = []
        
        success = False
        if file_type == 'audio/flac':
            success = self.parseFlac(song=song, artists=artistList, songModel=songModel, file_name=file_name, file_path=file_path)            
        elif file_type == 'audio/mp3':            
            success = self.parseMp3(song=song, songModel=songModel, artists=artistList, filename=file_name, filepath=file_path)
        else:
            print('处理失败: ' + file_name)
            Utils.set_label(file_path, ColorLabel.gray.value)
            return ''

        if success == False:
            return ''

        dbSongModel = self.songExist(songModel, artistList)
        if dbSongModel:
            print(f' {songModel.song_name} 数据库更新')
            # 数据库里已经存在了，为该首歌曲增加无损音乐数据
            if dbSongModel.sq_file_name == None and songModel.sq_file_name != None:
                dbSongModel.sq_file_name =songModel.sq_file_name
                dbSongModel.sq_file_path = songModel.sq_file_path
                print(f"更新 {dbSongModel.song_name}, 增加无损音乐: {songModel.sq_file_name}")            
            if dbSongModel.hq_file_name == None and songModel.hq_file_name != None:
                dbSongModel.hq_file_name = songModel.hq_file_name
                dbSongModel.hq_file_path = songModel.hq_file_path
                print(f"更新 {dbSongModel.song_name}, 增加高品质音乐: {songModel.hq_file_name}")
            dbSongModel.save()
        else:
            # 数据库里不存在，新建数据
            print(f' {songModel.song_name} 数据库新增!')
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
        """
        歌曲合法性校验，能不能通过mutagen进行解析
        """
        try:
            song = mutagen.File(file_path)
        except:
            print(f'[mutagen] 生成对象失败: {file_path}')
            return (False, None)
        else:
            return (True, song)

    def songExist(self, song: SongModel, artistList: list[ArtistModel]) -> SongModel:
        """
            数据库里有没有这首歌，歌名相同，歌手也相同            
        """

        # 先去数据库检查是否有这个名字的歌
        songModel = SongModel.objects.filter(song_name=song.song_name).first() 
        if songModel == None:
            return None

        # 再去找所有这个名字的歌手
        artistNames = list(map(lambda artist: artist.artist_name, artistList))
        artists = ArtistModel.objects.filter(artist_name__in=artistNames)
        artistsIds = list(map(lambda artist: artist.artist_id, artists))

        # 去关联表里面查一下，是不是这个歌的id 和 歌手的id是一样的 
        existArtistIds = Song2ArtistModel.objects.filter(song_id=songModel.song_id) 

        if set(artistsIds) == set(existArtistIds):
            print(f"数据库里已经有这首歌了 ")
            # 去检查歌手是不是也一样
            return songModel
        else:
            return None      
        
    def parseFlac(self, song, artists: list[ArtistModel], songModel: SongModel, file_name: str, file_path: str) -> bool:
        """
        解析flac音乐文件，把歌曲名，歌曲类型，文件路径，文件名设置到songModel数据模型中
        """
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
            self.parseArtist(artists, artist_name)
            return True
  
    def parseMp3(self, song, songModel: SongModel, artists: list[ArtistModel], filename: str, filepath: str) -> bool:
        """
            解析map3音乐文件，把歌曲名，歌曲类型，文件路径，文件名设置到songModel数据模型中
            解析歌手信息，存储到artists数组里面
        """
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
            self.parseArtist(artists, artist_name)
            return True
      
    def parseArtist(self, artistList: list[ArtistModel], name):                        
            artistName = ''
            if isinstance(name, list):
                if len(name) == 1:
                    artistName = name[0]
                    print(f'歌手名字列表: {name}, 歌手名字 = {artistName}')
                    print() 
                else:
                    print("多个歌手")
                    print(name) 
            elif isinstance(name, mutagen.id3.TPE1):                
                artistName = str(name.text[0]) if name.text else ""
                print(f'获取到歌手名字: {artistName} ')
            else:
                print(f'歌手名字: {name} 类型={type(name)}')
                artistName = name

            if artistName == '':
                return

            if '、' in artistName:
                artistList = self.splitArtist( artistName, '、', artistList)
            elif '/' in artistName:                
                artistList = self.splitArtist( artistName, '/', artistList)
            elif '&' in artistName:                
                artistList = self.splitArtist( artistName, '&', artistList)
            else:
                print(f"开始处理歌手：{artistName}")
                existArtist = self.findArtist(artist_name=artistName)
                if existArtist != None:
                    artistList.append(existArtist)
                else:
                    artist = ArtistModel()
                    artist.artist_name = artistName          
                    artistList.append(artist)
                
    def splitArtist(self, artistName, sep, artistList):
        nameList = artistName.split(sep)
        for nameItem in nameList:
            print(f"开始处理歌手：{nameItem}")
            existArtist = self.findArtist(artist_name=nameItem)
            if existArtist != None:
                artistList.append(existArtist)
            else:
                artist = ArtistModel()
                artist.artist_name = nameItem          
                artistList.append(artist)
        return artistList

    def findArtist(self, artist_name):
        """
        检查数据库是否有该歌手
        """
        artist = ArtistModel.objects.filter(artist_name=artist_name)
        if artist.count() > 0:
            print(f'歌手 {artist_name} 已经存在 ✅ ')
            return artist[0]
        else:
            print(f'歌手 {artist_name} 不存在 💡')
            return None

    def exist(self, filepath, filename) -> bool:
        return False
        if len(SongModel.objects.filter(sq_file_path=filepath)) > 0:
            return True
        elif len(SongModel.objects.filter(hq_file_path=filepath)) > 0:
            return True
        else:
            return False
        
        # color = Utils.get_file_label(filepath=filepath)
        if color == ColorLabel.green:
            return True
        else:
            return False
        

""" 
1. 遍历音乐根目录 
2. 过滤掉.DS_Store 和 lrc文件 
3. 拿到文件名，拼接得到文件路径
4. 通过文件名和文件路径在数据库中检查，数据库中是否已经存在 [‼️ 暂未处理]
5. 创建歌曲的数据模型 songModel 和 歌手列表 artists
6. 解析歌曲
    1. 用mutagen去解析这个文件 ；解析失败 - 将文件设置一个灰色标签，结束对这个文件的处理 
    2. 读取音乐的类型: flac / mp3 ; （其他的类型暂时未处理）
    3. 根据文件类型，读取歌曲名和歌手信息
    4. 把歌曲名放到songModel
    5. 处理歌手
        1. 如果歌手名字包含了 '、' ，用 '、'切割字符串，遍历所有的歌手名字 
        2. 去AritistModel的数据库查询是否有这个名字的歌手，如果有，拿到歌手数据模型；如果没有，创建一个新的歌手数据模型。放到歌手列表的数组里面
7. 去SongModel数据库查询是否有该名字的歌曲，如果找到了检查歌手和当前歌曲的歌手是不是一样 
8. 如果已经存在了这首歌，把高品质的路径添加到这首歌的数据表里
9. 如果不存在，把SongModel进行保存
    
"""

class Songs(View):

    def get(self, request):
        pass

class Search(View):
    def get(self, request):
        queryWord = request.GET.get('query')
