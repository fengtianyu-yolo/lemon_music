from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from django.views import View
from django.core.serializers import serialize
from enum import Enum
import json

import mutagen.id3
from .models import SongModel, ArtistModel, Song2ArtistModel
import os
import subprocess
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

    failList = []
    successList = []
    fullList = []

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
            else:
                print(f"{item} 文件处理失败 ❓ \n")
        
        print('处理文件数量: ' + str(len(result)))
        print(self.successList)
        print(self.failList)
        print('处理失败歌曲数量: ' + str(len(self.failList)))
        print('插入成功歌曲数量: ' + str(len(self.successList)))
        print('全格式歌曲数量: ' + str(len(self.fullList)))
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
            # 数据库里已经存在了，为该首歌曲增加无损音乐数据
            print(f"🎵 无损音乐='{dbSongModel.sq_file_path}', HQ='{dbSongModel.hq_file_path}'")            
            if dbSongModel.sq_file_path == '' and songModel.sq_file_path != '':
                dbSongModel.sq_file_name =songModel.sq_file_name
                dbSongModel.sq_file_path = songModel.sq_file_path
                print(f"🎵 更新 {dbSongModel.song_name}, 增加无损音乐: {songModel.sq_file_name}")            
                dbSongModel.save()
                Utils.set_label(file_path, ColorLabel.green.value)
                print(f"🛢️ '{songModel.song_name}' 数据库更新 🔄")
                self.fullList.append(dbSongModel.song_name)
            elif dbSongModel.hq_file_path == '' and songModel.hq_file_path != '':
                dbSongModel.hq_file_name = songModel.hq_file_name
                dbSongModel.hq_file_path = songModel.hq_file_path
                print(f"🎵 更新 {dbSongModel.song_name}, 增加高品质音乐: {songModel.hq_file_name}")
                dbSongModel.save()
                Utils.set_label(file_path, ColorLabel.green.value)
                print(f"🛢️ '{songModel.song_name}' 数据库更新 🔄")
                self.fullList.append(dbSongModel.song_name)
            else:
                if dbSongModel.sq_file_path != '' and songModel.sq_file_path != '':
                    print(f"🛢️ 更新失败: 重复歌曲 db.hq_path={dbSongModel.sq_file_path}, song.hq={songModel.sq_file_path} ❌")
                    self.failList.append(songModel.song_name)
                    Utils.set_label(file_path, ColorLabel.yellow.value)
                elif dbSongModel.hq_file_path != '' and songModel.hq_file_path != '':
                    print(f"🛢️ 更新失败: 重复歌曲 db.hq_path={dbSongModel.hq_file_path}, song.hq={songModel.hq_file_path} ❌")
                    self.failList.append(songModel.song_name)
                    Utils.set_label(file_path, ColorLabel.yellow.value)
                else:
                    print(f"🛢️ 更新失败: db.sq={dbSongModel.sq_file_path} db.hq={dbSongModel.hq_file_path} song.sq={songModel.sq_file_path} song.hq={songModel.hq_file_path} ❌")
                    self.failList.append(songModel.song_name)
                    Utils.set_label(file_path, ColorLabel.yellow.value)
        else:
            # 数据库里不存在，新建数据
            print(f"🛢️ '{songModel.song_name}' 数据库新增! 🚩 \n")
            duration = song.info.length
            songModel.duration = duration
            songModel.save() 
            Utils.set_label(file_path, ColorLabel.green.value)
            self.successList.append(songModel.song_name)
            for artist in artistList:
                songArtistModel = Song2ArtistModel() 
                songArtistModel.song = songModel 
                songArtistModel.artist = artist            
                artist.save() 
                songArtistModel.save()             
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
            print('🛢️ 数据库未找到同名歌曲 🚫')
            return None

        # 再去找所有这个名字的歌手
        artistNames = list(map(lambda artist: artist.artist_name, artistList))
        artists = ArtistModel.objects.filter(artist_name__in=artistNames)
        artistsIds = list(map(lambda artist: artist.artist_id, artists))

        # 去关联表里面查一下，是不是这个歌的id 和 歌手的id是一样的 
        existModels = Song2ArtistModel.objects.filter(song_id=songModel.song_id) 
        existArtistIds = list(map(lambda model: model.artist.artist_id, existModels))

        if set(artistsIds) == set(existArtistIds):
            print(f"🛢️ 数据库里已经有这首歌了 ids={artistsIds}; exist={existArtistIds} 👀")
            # 去检查歌手是不是也一样
            return songModel
        else:
            print(f'🛢️ 数据库有同名歌曲，🧑‍🎤歌手不同 当前歌手={artistsIds} 已存储歌曲的歌手={existArtistIds} 🚫')
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
            if isinstance(song_name, list) and len(song_name) > 0:
                song_name = str(song_name[0])            
            songModel.song_name = song_name.strip()
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
            if isinstance(song_name, mutagen.id3.TIT2):
                song_name = str(song_name.text[0])
            songModel.song_name = song_name.strip()
            songModel.media_type = MediaType.MP3.value 
            songModel.hq_file_path = filepath 
            songModel.hq_file_name = filename
            self.parseArtist(artists, artist_name)
            return True
      
    def parseArtist(self, artistList: list[ArtistModel], name):                        
            artistName = ''
            if isinstance(name, list):
                if len(name) == 1:
                    artistName = name[0].strip()
                    print(f'歌手名字列表: {name}, 歌手名字 = {artistName}')
                else:
                    print("多个歌手")
                    print(name) 
            elif isinstance(name, mutagen.id3.TPE1):                
                artistName = str(name.text[0]).strip() if name.text else ""
                print(f'获取到歌手名字: {artistName} ')
            else:
                print(f'歌手名字: {name} 类型={type(name)}')
                artistName = name.strip()

            if artistName == '':
                return

            if '、' in artistName:
                artistList = self.splitArtist( artistName, '、', artistList)
            elif '/' in artistName:                
                artistList = self.splitArtist( artistName, '/', artistList)
            elif '&' in artistName:                
                artistList = self.splitArtist( artistName, '&', artistList)
            else:
                print(f"🧑‍🎤 开始处理歌手：{artistName}")
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
            print(f"🧑‍🎤 开始处理歌手：{nameItem}")
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
            print(f'🧑‍🎤 歌手 {artist_name} 已经存在 ✅ ')
            return artist[0]
        else:
            print(f'🧑‍🎤 歌手 {artist_name} 不存在 🚫')
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
    

数据检查： 
重复歌曲未插入数据库的数量 + 数据库中行数 + hq+sq都有的歌曲的数量 = 文件数量
"""

class Songs(View):

    def get(self, request):
        songList = []
        response = {'data': []}

        songs = SongModel.objects.all()
        for song in songs:
            
            songDict = {
                'song_name': song.song_name,
                'song_id': song.song_id,
                'duration': song.duration,
                'media_type': song.media_type,
                'cover_path': song.cover_path,
                'sq_file_path': song.sq_file_path,
                'hq_file_path': song.hq_file_path,
                'sq_file_name': song.sq_file_name,
                'hq_file_name': song.hq_file_name
            }
            artists = Song2ArtistModel.objects.filter(song=song)
            artistDicts = []            
            for user in artists:
                artistDict = {
                    'artist_name': user.artist.artist_name,
                    'artist_id': user.artist.artist_id
                }
                artistDicts.append(artistDict)
            songDict['artists'] = artistDicts
            songList.append(songDict)
        response['data'] = songList
        print(response)
        return JsonResponse(response)
        # serializeData = serialize('json', songs)
        # data = json.loads(serializeData)
        # finaData = [item['fields'] for item in data]
        # print(finaData)
        # return JsonResponse({'songs': finaData})

class Search(View):
    def get(self, request):
        queryWord = request.GET.get('query')


HLS_CACHE = '/Users/fengtianyu/Projects/lemon_music/hls_cache'

class StreamView(View):

    def get(self, request, filename):
        input_file = '/Volumes/MdieaLib/音乐库/音乐/2021/01/01/01/01.mp3'
        output_dir = '/Volumes/MdieaLib/音乐库/音乐/2021/01/01/01/hls'
        output_m3u8 = self.create_hls(input_file, output_dir)
        return JsonResponse({'m3u8': output_m3u8})

    def stream_audio(self, request, filename):
        """
        返回m3u8文件
        """
        input_file = '/Volumes/MdieaLib/音乐库/音乐/2021/01/01/01/01.mp3'
        if not os.path.exists(input_file):
            return JsonResponse({'code': 404, 'msg': '文件不存在'})
        
        # HLS 分片目录
        output_dir = os.join(HLS_CACHE, filename.split('.')[0])
        m3u8_path = os.join(output_dir, 'index.m3u8')

        # 生成m3u8文件
        self.create_hls(input_file, output_dir)
        with open(m3u8_path, 'r') as f:
            m3u8_content = f.read()
        return HttpResponse(m3u8_content, content_type='application/vnd.apple.mpegurl')


    def stream_segment(self, request, filename, segment):
        """
        返回ts文件 hls分片
        """
        input_file = '/Volumes/MdieaLib/音乐库/音乐/2021/01/01/01/01.mp3'
        if not os.path.exists(input_file):
            return JsonResponse({'code': 404, 'msg': '文件不存在'})
        
        output_dir = os.join(HLS_CACHE, filename.split('.')[0])
        segment_file = os.join(output_dir, f'{segment}.ts')
        with open(segment_file, 'rb') as f:
            segment_content = f.read()
        return HttpResponse(segment_content, content_type='video/mp2t')


    def create_hls(input_file, output_dir, segment_time=10):
        """
        创建hls文件
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_m3u8 = f'{output_dir}/index.m3u8'
        command = [
            'ffmpeg',
            '-i', input_file,
            '-codec: audio', 'aac',
            '-b:a', '128k',
            '-f', 'hls',
            '-hls_time', str(segment_time),
            '-hls_playlist_type', 'vod',
            '-hls_list_size', '0',
            '-hls_segment_filename', f'{output_dir}/%03d.ts',
            f'{output_dir}/index.m3u8'
        ]
        # command = f'ffmpeg -i {input_file} -hls_time {segment_time} -hls_list_size 0 -hls_segment_filename {output_dir}/%03d.ts {output_dir}/index.m3u8'
        print(command)
        subprocess.run(command, check=True)
        return output_m3u8

class StreamAudio(StreamView):
    def get(self, request, filename):
        return self.stream_audio(request, filename)


class StreamSegment(StreamView):
    def get(self, request, filename, segment):
        return self.stream_segment(request, filename, segment)