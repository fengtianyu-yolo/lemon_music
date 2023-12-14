from typing import Any
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.db import models
from django.forms.models import model_to_dict

import json
import os
from tinytag import TinyTag
import hashlib
import datetime
import time

from .models import SongModel
from .models import SingerModel
from .MediaType import MediaType

# Create your views here.

class Test(View):
    def get(self, request):
        result = {
            'code': 0,
            'message': '测试成功'
        }
        return HttpResponse(json.dumps(result))

class Login(View):
    
    TEMPLATE = 'login.html'

    def get(self, request):
        return render(request, template_name=self.TEMPLATE)
    
    def post(self, request):
        username = request.POST.get('username')
        print(username)

        return redirect('dashboard')
    
class LoginAPI(View):

    def get(self, request):
        result = {
            'code': 0,
            'data': {
                'user_id': '123',
                'username': '小困子',
                'avatar': '',
                'token': '12312312312'
            }            
        }
        return HttpResponse(json.dumps(result))

class Dashboard(View):

    def get(self, request):
        songs = SongModel.objects.all().order_by('created_time')
        song_count = songs.count()
        lastUpdate = songs[0].created_time
        print(f"last update = {lastUpdate}")            
        
        # 拿到最近的周一0点的时间戳 
        today = datetime.date.today() # 今天 
        now = datetime.datetime.now().weekday()
        monday = today - datetime.timedelta(days=now) # 获取周一的日期
        monday_time = datetime.datetime(monday.year, monday.month, monday.day, 0, 0, 0) # 拿到周一0点的时间戳 
        new_add_in_week = SongModel.objects.filter(created_time__gt=monday_time).count()

        singer_count = SingerModel.objects.all().count()

        song_card = {
            'title': '歌曲',
            'last_update': lastUpdate,
            'new_add': new_add_in_week,
            'count': song_count,
            'card_type': 0
        }

        singer_card = {
            'title': '歌手',
            'last_update': 12,
            'new_add': 12,
            'count': singer_count,
            'card_type': 1
        }

        result = {
            'code': 0,
            'data': [
                song_card,
                singer_card
            ]
        }
        return HttpResponse(json.dumps(result))


class SongList(View):

    def get(self, request):
        songs = SongModel.objects.all()
        items = []
        for item in songs:
            singers = []
            for singer in item.singers.all():
                dict = model_to_dict(singer)
                singers.append(dict)
            model_dic = model_to_dict(item)
            model_dic['singers'] = singers
            items.append(model_dic)
        
        result = {
            'code': 0,
            'list': items
        }
        print(result)
        return HttpResponse(json.dumps(result))

class Search(View):
    def get(self, request): 
        search_name = request.GET.get('name') 
        
        datas = SongModel.objects.filter(song_name__contains=search_name)
        items = []
        for item in datas:
            singer_dic = model_to_dict(item.singer)
            model_dic = model_to_dict(item)
            model_dic['singer'] = singer_dic
            items.append(model_dic)
        
        result = {
            'code': 0,
            'list': items
        }
        return HttpResponse(json.dumps(result))


class RefreshList(View):

    unsupport_files = []

    # 支持处理的音乐格式
    support_files = ['wav', 'ape', 'mp3', 'flac']

    # 曲库目录
    path = '/Volumes/Elements SE/音乐库'

    def get(self, request):
        self.refresh()
        result = {
            'code': 0,
            'data': {
                'list': []
            }
        }        
        return HttpResponse(json.dumps(result)) 
    

    def refresh(self): 
        # 拿到曲库下的所有文件
        song_list = os.listdir(self.path)                

        # 拿到所有已入库的歌曲的id；从对象数组提取对象的属性并转成数组 list(map(lambda obj: obj.xx, obj_list))
        songs = SongModel.objects.all()
        self.song_ids = list(map(lambda song: song.song_id, songs))
        print(f"song_id_list = {self.song_ids}")
        
        # 2 遍历所有的文件  
        for song_name in song_list:    
            # 拿到文件路径
            file_path = self.path + '/' + song_name
            self.write_to_normallog(f'获取到文件路径 {file_path}')

            # 拿到文件的后缀名，检查是否为支持的文件  
            suffix = file_path.split('.')[-1]
            self.write_to_normallog(f'文件后缀 {suffix}')

            if suffix in self.support_files and self.exist(file_path) == False:
                self.parse_file(file_path)
            else:
                if self.exist(file_path) == False:
                    self.write_to_normallog(f'文件已录入 {file_path}')
                else:
                    self.write_to_log(f'不支持的文件 {file_path}')
                self.write_to_normallog("\n\n")
                continue

            self.write_to_normallog("\n\n")


    def exist(self, file_path) -> bool:
        """
        文件是否已经在数据库中存在
        """
        # 获取文件的MD5 
        file_hash_value = self.checksum(file_path)
        # 文件在数据库中是否已经存在；已存在则跳过，不存在则插入到数据库 
        _exist = file_hash_value in self.song_ids
        return _exist


    def parse_file(self, file):
        """
        处理音乐文件
        """
        if file.endswith('mp3'):
            self.parse_mp3(file)
        elif file.endswith('flac'):
            self.parse_flac(file)
        elif file.endswith('ape'):
            self.parse_wav_and_ape(file)
        elif file.endswith('wav'):
            self.parse_wav_and_ape(file)
        else:
            print(f"未知的文件类型 {file}")


    def create_song(self, file_path, song_name, format, duration, singers):
        song = SongModel()
        song_id = self.checksum(file_path)
        song.song_id = song_id
        song.song_name = song_name 
        song.media_type = format 
        song.duration = duration         
        song.file_path= file_path 
        song.file_md5 = song_id
        song.save()
        song.singers.set(singers)
        song.save()
        self.write_to_normallog(f'歌曲创建成功 = {song_name}、{format}、{duration}、{singers}')
    

    def parse_mp3(self, file):
        """
        解析MP3文件
        """
        self.write_to_normallog(f'处理MP3文件')
        info = TinyTag.get(file)
        song_name = info.title 
        duration = info.duration 
        format = 'mp3'
        artist = info.artist
        if artist == None or song_name == None:
            self.parse_exception_flac(file)
            return
                
        singers = self.get_singers(artist)

        self.create_song(file, song_name, format, duration, singers)        


    def parse_wav_and_ape(self, file):
        self.write_to_normallog(f"解析wav文件")
        # 拿到文件名
        file_name = file.split('/')[-1]
        file_name = file_name.split('.')[0]
        self.write_to_normallog(f"歌曲名 = {file_name}")

        # 切割文件名
        names = file_name.split('-')
        
        if len(names) != 2: 
            print("文件名解析失败")
            self.write_to_normallog(f"wav文件名字解析失败")
            self.write_to_log(f"{file} > 未能解析")
            return
        
        song_name = names[-1].strip()
        singer_name = names[0].strip()

        format = 'wav'
        if file.endswith('wav'):
            format = 'wav'
        elif file.endswith('ape'):
            format = 'ape'
            
        duration = 0
        try:
            tag = TinyTag.get(file)
            duration = tag.duration
        except:
            duration = 0
        
        singers = self.get_singers(singer_name)

        self.create_song(file, song_name, format, duration, singers)


    def parse_flac(self, file):
        self.write_to_normallog(f'处理FLAC文件')
        try:
            tag = TinyTag.get(file)
            # 获取文件的MD5 
            file_hash_value = self.checksum(file)
            song_name = tag.title
            singer_names = tag.artist 
            
            if song_name == None or singer_names == None:
                self.write_to_normallog(f'没有拿到FLAC的 title 或 singer')
                self.parse_exception_flac(file=file)
                return
            
            format = 'flac'
            duration = tag.duration
            singer_models = self.get_singers(singer_names)
            self.create_song(file, song_name, format, duration, singer_models)
                        
        except Exception as e:
            self.parse_exception_flac(file=file)
        
    
    def parse_exception_flac(self, file):
        """
        处理异常的flac文件
        """
        self.write_to_normallog(f'处理异常的FLAC文件')
        # 拿到文件名
        file_name = file.split('/')[-1]
        file_name = file_name.split('.')[0] # 去掉后缀 
        self.write_to_normallog(f"歌曲名 = {file_name}")

        # 切割文件名
        names = file_name.split('-')
        if self.is_singer_name(names[0].strip()):
            singer_names = names[0].strip()
            song_name = names[-1].strip()
        elif self.is_singer_name(names[-1].strip()):
            singer_names = names[-1].strip()
            song_name = names[0].strip()
        else:
            self.write_to_log(f"{file} > 未能解析")
            return
        
        singer_models = self.get_singers(singer_names)
        duraion = 0
        try: 
            info = TinyTag.get(file)
            duraion = info.duration
        except Exception as e:
            self.write_to_log(f"{file}: {e}")
            return

        format = file.split('.')[-1]
        self.create_song(file, song_name, format, duraion, singer_models)
    

    def get_singers(self, artists) -> [SingerModel]:
        """
        获取这首歌的所有歌手
        """
        
        self.write_to_normallog(f'解析歌手 = {artists}')
        
        singer_names = []
        if '、' in artists:
            singer_names = artists.split('、')
            self.write_to_normallog(f'有多个歌手，已经分离出来= {singer_names}')
        elif '&' in artists:
            singer_names = artists.split('&')
            self.write_to_normallog(f'有多个歌手，已经分离出来= {singer_names}')
        elif ',' in artists:
            singer_names = artists.split(',')
            self.write_to_normallog(f'有多个歌手，已经分离出来= {singer_names}')
        else:
            # 只有一个歌手
            singer_names = [artists]
            self.write_to_normallog(f'只有一个歌手 {singer_names}')
        
        singer_models = []
        for singer in singer_names:
            singer_model = SingerModel.objects.filter(singer_name=singer)
            if singer_model != None and len(singer_model.all()) > 0:
                # 歌手已经存在
                singer_models.append(singer_model.all()[0])
                self.write_to_normallog(f'该歌手已经存在 = {singer_model}')
            else:
                # 歌手不存在，创建歌手对象
                singer_model = SingerModel() 
                singer_model.singer_name = singer
                singer_model.save()
                singer_models.append(singer_model)
                self.write_to_normallog(f'创建新歌手 = {singer_model}')
        
        return singer_models


    def is_singer_name(self, name) -> bool:
        """
        检查是否有该名字的歌手
        """
        if ',' in name:
            return True
        elif '、' in name:
            return True
        elif '&' in name:
            return True
        else:
            return SingerModel.objects.filter(singer_name=name).exists()
        

    def file_format(self, file_name: str) -> str:
        suffix = file_name.split('.')[-1]
        return suffix


    def checksum(self, filename):
        """
        获取大文件的哈希值
        """
        file_hash = hashlib.md5()
        with open(filename, 'rb') as f:
            while chunk := f.read(8192):
                file_hash.update(chunk)
        
        return file_hash.hexdigest()
    
    def write_to_log(self, content):
        with open('./log.txt', 'a+') as f:
            f.write(content)
            f.write('\n')

    def write_to_normallog(self, content):
        with open('./normal_log.txt', 'a+') as f:
            f.write(content)
            f.write('\n')
            print(content)
