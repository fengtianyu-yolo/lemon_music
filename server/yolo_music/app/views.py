from django.shortcuts import render
from django.http import HttpResponse 
from django.http import JsonResponse
from django.views import View
from django.core.serializers import serialize
from enum import Enum
import json
import mutagen.id3
from rest_framework.views import APIView
import os
import subprocess
import mutagen
from .Utils import Utils, ColorLabel
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Song, Artist, File, Tag
from django.core.files.base import ContentFile

from yolo_music import settings
from .models import SongModel, ArtistModel, Song2ArtistModel
from .models import Artist, Tag, File, Song
from datetime import datetime

# Refactor 

class Logger:
    def __init__(self):
        self.log_dir = '/Users/fengtianyu/Projects/lemon_music/server/yolo_music/logs'
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        self.log_file = os.path.join(
            self.log_dir, 
            f'music_scanner_{datetime.now().strftime("%Y%m%d")}.log'
        )
    
    def log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f'[{timestamp}] {message}\n')

    def info(self, message):
        self.log(f'[INFO] {message}')
    
    def error(self, message):
        self.log(f'[ERROR] {message}')
    
    def warning(self, message):
        self.log(f'[WARNING] {message}')
    
    def write_unknown_file(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_dir = '/Users/fengtianyu/Projects/lemon_music/server/yolo_music/unknown_file.txt'
        with open(log_dir, 'a', encoding='utf-8') as f:
            f.write(f'[{timestamp}] {message}\n')
    
    def write_parsefailed_file(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_dir = '/Users/fengtianyu/Projects/lemon_music/server/yolo_music/parse_failed.txt'
        with open(log_dir, 'a', encoding='utf-8') as f:
            f.write(f'[{timestamp}] {message}\n')
    
    def write_handlefailed_file(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_dir = '/Users/fengtianyu/Projects/lemon_music/server/yolo_music/handle_failed.txt'
        with open(log_dir, 'a', encoding='utf-8') as f:
            f.write(f'[{timestamp}] {message}\n')
    
    def write_success_file(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_dir = '/Users/fengtianyu/Projects/lemon_music/server/yolo_music/success.txt'
        with open(log_dir, 'a', encoding='utf-8') as f:
            f.write(f'[{timestamp}] {message}\n')
    
    def write_nosinger_file(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_dir = '/Users/fengtianyu/Projects/lemon_music/server/yolo_music/no_singer.txt'
        with open(log_dir, 'a', encoding='utf-8') as f:
            f.write(f'[{timestamp}] {message}\n')        

class MusicScanner(APIView):
    
    def __init__(self):
        super().__init__()
        self.logger = Logger()

    def get(self, request):
        root_path = '/Volumes/MdieaLib/音乐库'
        for root, dirs, files in os.walk(root_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(('.mp3', '.flac', '.ape', '.wav')):
                    self._process_audio_file(file_path)      
                else:
                    self.logger.write_unknown_file(f'Not audio file: {file_path}')

        return Response({"message": "ok"}, status=200)

    def _process_audio_file(self, file_path):
        try:
            # 解析音频文件
            audio = mutagen.File(file_path, easy=True)
            if not audio:
                self.logger.write_parsefailed_file(f'无法解析音频文件: {file_path}')
                return

            # 获取基本信息
            title = audio.get('title', [os.path.splitext(os.path.basename(file_path))[0]])[0]
            artist_names = audio.get('artist', [])
            
            # 如果没有获取到标题和歌手信息，检查是否为 wav 文件
            if (not title or not artist_names) and file_path.lower().endswith('.wav'):
                file_name = os.path.splitext(os.path.basename(file_path))[0]
                if '-' in file_name:
                    parts = file_name.split('-', 1)  # 只分割第一个'-'
                    if len(parts) == 2:
                        artist_names = [parts[0].strip()]
                        title = parts[1].strip()

            # 如果没有歌手信息，记录日志并返回
            if not artist_names:
                self.logger.write_nosinger_file(f'无法获取歌手信息: {file_path}')
                return
                
            duration = int(audio.info.length) if hasattr(audio.info, 'length') else 0
            format_type = os.path.splitext(file_path)[1][1:].lower()
            file_size = os.path.getsize(file_path)

            # 创建或获取 Artist 对象
            artists = []
            if artist_names:
                # 处理可能的多个歌手名字
                if isinstance(artist_names, list):
                    raw_artist = artist_names[0]
                else:
                    raw_artist = artist_names
                
                # 处理不同的分隔符
                if '、' in raw_artist:
                    artist_list = raw_artist.split('、')
                elif '/' in raw_artist:
                    artist_list = raw_artist.split('/')
                elif '&' in raw_artist:
                    artist_list = raw_artist.split('&')
                else:
                    artist_list = [raw_artist]
                
                # 为每个歌手创建记录
                for name in artist_list:
                    name = name.strip()
                    if name:
                        artist, _ = Artist.objects.get_or_create(name=name)
                        artists.append(artist)

            # 创建或获取 Song 对象
            song, created = Song.objects.get_or_create(
                title=title,                
                defaults={
                    'duration': duration,
                    'play_count': 0  # 新歌曲播放次数初始化为0
                }
            )

            # 设置歌手
            song.artists.set(artists)

            # 创建 File 对象
            file_obj, _ = File.objects.get_or_create(
                file_path=file_path,
                defaults={
                    'song': song,
                    'file_size': file_size,
                    'format_type': format_type
                }
            )

            # 处理封面（如果是MP3文件）
            if format_type == 'mp3':
                try:
                    mp3_file = mutagen.mp3.MP3(file_path)
                    for tag in mp3_file.tags.values():
                        if tag.FrameID == 'APIC':
                            cover_file = ContentFile(tag.data)
                            song.cover.save(f'cover/{title}.jpg', cover_file, save=True)
                            break
                except Exception as e:
                    print(f"提取封面失败: {e}")

            self.logger.write_success_file(f'成功处理音频文件: {file_path}')

        except Exception as e:
            self.logger.write_handlefailed_file(f'处理文件失败: {file_path} {str(e)}')            


    def _get_or_create_artist(self, names):
        artist_objs = []
        # for artist_name in names:
        #     artist, _ = Artist.objects.get_or_create(name=artist_name)
        #     artist_objs.append(artist)
        return artist_objs

    def _get_or_create_song(self, title, artist_objs, format):
        song_qs = Song.objects.filter(title=title)
        for artist_obj in artist_objs:
            song_qs = song_qs.filter(artists==artist_obj)
        
        if song_qs.exists():
            song = song_qs.first()
        else:
            song = Song.objects.create(title=title)
            # 如果是 MP3 文件，尝试提取封面
            if format == 'mp3':
                try:
                    # 使用 mutagen.mp3 读取文件
                    audio = mutagen.mp3.MP3(file_path)
                    # 获取 APIC 标签（专辑封面）
                    for tag in audio.tags.values():
                        if tag.FrameID == 'APIC':
                            # 创建一个临时文件名
                            cover_filename = f"covers/{title}_{hash(str(artist_objs))}.jpg"
                            # 使用 ContentFile 创建文件对象
                            cover_file = ContentFile(tag.data)
                            # 保存封面图片
                            song.cover.save(cover_filename, cover_file, save=True)
                            break
                except Exception as e:
                    print(f"提取封面失败: {e}")
            
            song.artists.set(artist_objs)
        return song

    def _get_or_create_tag(self, names):
        tag_objs = []
        for tag_name in names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_objs.append(tag)
        return tag_objs



@api_view(['GET'])
def get_tags(request):
    tags = Tag.objects.all()
    tag_list = []
    for tag in tags:
        tag_list.append(tag.name)
    return JsonResponse({'code': 200, 'data': tag_list})

@api_view(['POST'])
def create_tag(request):
    """ 创建标签 """
    name = request.data.get('name')
    if not name:
        return Response({'code': 400,'message': 'Name is required'}, status=400)
    tag, created = Tag.objects.get_or_create(name=name)
    if created:
        return Response({'code': 200, 'message': 'Tag created successfully', 'data': tag.name}, status=200)
    else:
        return Response({'code': 200,'message': 'Tag already exists', 'data': tag.name}, status=200)

@api_view(['DELETE'])
def delete_tag(request, tag_id):
    """ 删除标签 """
    try:
        tag = Tag.objects.get(id=tag_id)
        tag.delete()
        return Response({'code': 200,'message': 'Tag deleted successfully'}, status=200)
    except Tag.DoesNotExist:
        return Response({'code': 404, 'message': 'Tag not found'}, status=404)

@api_view(['GET'])
def get_all_songs(request):
    songs = Song.objects.all()
    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data)    

@api_view(['GET'])
def add_tag_to_song(request):
    pass

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


HLS_CACHE = '/Users/fengtianyu/Projects/lemon_music/server/yolo_music/media_cache'
MEDIA_ROOT = '/Volumes/MdieaLib/音乐库'

class StreamView(View):

    def get(self, request, filename):
        input_file = '/Volumes/MdieaLib/音乐库/音乐/2021/01/01/01/01.mp3'
        output_dir = '/Volumes/MdieaLib/音乐库/音乐/2021/01/01/01/hls'
        output_m3u8 = self.create_hls(input_file, output_dir)
        return JsonResponse({'m3u8': output_m3u8})

    def stream_audio(self, request):
        """
        返回m3u8文件
        """
        input_file = request.GET.get('filepath')
        input_file = str(input_file)        
        print(type(input_file))
        """
        if filepath:
            input_file = filepath
        else:
            input_file = os.path.join(MEDIA_ROOT, filename)
            print(f"get input file: {0}", input_file)
            if not os.path.exists(input_file):
                return JsonResponse({'code': 404, 'msg': '文件不存在'})
        """
        
        if not os.path.exists(input_file):
            return JsonResponse({'code': 404, 'msg': '文件不存在'})
        
        # if len(filename) == 0:
        filename = input_file.split('/')[-1]
        print(filename)

        # HLS 分片目录        
        output_dir = os.path.join(HLS_CACHE, filename.replace('.', '-'))
        m3u8_path = os.path.join(output_dir, 'index.m3u8')

        # 生成m3u8文件
        m3u8_url = self.create_hls(input_file, output_dir)
        
        return JsonResponse({"m3u8_url": request.build_absolute_uri(m3u8_url)})
    
        # return JsonResponse({'m3u8': m3u8_path})
        with open(m3u8_path, 'r') as f:
            m3u8_content = f.read()        
        return HttpResponse(m3u8_content, content_type='application/vnd.apple.mpegurl')


    def stream_segment(self, request, filename, filepath, segment):
        """
        返回ts文件 hls分片
        """
        # if request.GET.get('segment'):
        segment = request.GET.get('segment')
        input_file = request.GET.get('filepath')

        """
        if filepath:
            input_file = filepath
        else:
            input_file = os.path.join(MEDIA_ROOT, filename)

        if len(filename) == 0:
            filename = filepath.split('/')[-1]
        """

        if not os.path.exists(input_file):
            return JsonResponse({'code': 404, 'msg': '文件不存在'})
        
        output_dir = os.join(HLS_CACHE, filename.split('.')[0])
        segment_file = os.join(output_dir, f'{segment}.ts')
        with open(segment_file, 'rb') as f:
            segment_content = f.read()
        return HttpResponse(segment_content, content_type='video/mp2t')


    def create_hls(self, input_file: str, output_dir: str, segment_time=10):
        """
        创建hls文件
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        temp_file = f'{output_dir}/intermediate.wav'
        tmp_command = [
            'ffmpeg',
            '-i', input_file,
            '-c:a', 'pcm_s16le',
            '-ar', '44100',
            temp_file
        ]
        subprocess.run(tmp_command, check=True)

        output_m3u8 = f'{output_dir}/index.m3u8'
        command = [
            'ffmpeg',
            '-i', temp_file,
            '-c:a', 'aac',
            '-c:v', 'copy',
            '-b:a', '128k',
            '-f', 'hls',
            '-hls_time', str(segment_time),
            '-hls_playlist_type', 'vod',
            '-hls_list_size', '0',
            '-hls_segment_filename', f'{output_dir}/%03d.ts',
            output_m3u8
        ]        
        subprocess.run(command, check=True)
        # return output_m3u8

        relative_path = os.path.relpath(output_m3u8, settings.MEDIA_ROOT)
        return f"{settings.MEDIA_URL}{relative_path}"
        

class StreamAudio(StreamView):
    def get(self, request, filename):
        return self.stream_audio(request, filename)
    
    def get(self, request):
        return self.stream_audio(request)


class StreamSegment(StreamView):
    def get(self, request, filename, segment):        
        return self.stream_segment(request, filename, segment)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SongSerializer

@api_view(['GET'])
def get_song_list(request):
    songs = Song.objects.all().prefetch_related('artists', 'files')
    serializer = SongSerializer(songs, many=True)
    return Response({
        'code': 200,
        'data': serializer.data
    })