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

from .models import SongModel
from .models import SingerModel
from .MediaType import MediaType

# Create your views here.

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

class SongList(View):

    def get(self, request):
        songs = SongModel.objects.all()
        items = []
        for item in songs:
            singer_dic = model_to_dict(item.singer)
            model_dic = model_to_dict(item)
            model_dic['singer'] = singer_dic
            items.append(model_dic)
        
        result = {
            'code': 0,
            'list': items
        }
        return HttpResponse(json.dumps(result))

class Search(View):
    def get(self, request): 
        search_name = request.GET.get('name') 
        
        datas = SongModel.objects.filter(song_name=search_name)
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

        # 拿到目录下的所有文件 
        path = '/Volumes/Elements SE/音乐库'
        song_list = os.listdir(path)

        # 拿到数据库所有文件的id；从对象数组提取对象的属性并转成数组 list(map(lambda obj: obj.xx, obj_list))
        songs = SongModel.objects.all()
        song_ids = list(map(lambda song: song.song_id, songs))
        print(f"song_id_list = {song_ids}")
        
        # 2 遍历所有的文件  
        for song_name in song_list:    
            file_path = path + '/' + song_name
    
            try:
                tag = TinyTag.get(file_path)
                # 获取文件的MD5 
                file_hash_value = self.checksum(file_path)
                                
                # 文件在数据库中是否已经存在；已存在则跳过，不存在则插入到数据库 
                exist = file_hash_value in song_ids
                
                if not exist:
                    # 歌手是否已经存在
                    self.update_singer(tag)     
                    # 更新歌曲信息
                    self.update_song(tag, file_hash_value, file_path, song_name)
                
            except Exception as e:
                print(f"Error reading audio info: {e} {song_name}")
                self.unsupport_files.append(song_name)
                # 记录未解析文件 
        

    def update_song(self, song_info: TinyTag, id: int, file_path: str, file_name: str):
        """
        更新歌曲到数据库
        """
        if song_info.title == None:
            print(f"文件解析失败 = {file_name}")
            self.unsupport_files.append(file_name)
        else:
            song_name = song_info.title
            singer = song_info.artist 
            duration = song_info.duration
            
            song = SongModel()
            song.song_id = id
            song.song_name = song_name
            song.media_type = self.file_format(file_name)
            song.duration = duration
            song.file_path = file_path
            song.file_md5 = id
            song.singer = SingerModel.objects.get(singer_name=singer)
            song.save()
            

    def update_singer(self, song_info: TinyTag):
        singer = song_info.artist
        if song_info.artist == None:
            print(f'无法解析到歌手信息 {song_info}')
            return
        
        if not SingerModel.objects.filter(singer_name=singer).exists():
            singer_model = SingerModel() 
            singer_model.singer_name = singer
            singer_model.save()
        else:
            print(f"歌手已存在 {singer}")
        

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
    
