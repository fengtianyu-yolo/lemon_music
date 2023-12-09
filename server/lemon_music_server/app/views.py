from typing import Any
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect

import json
import os
from tinytag import TinyTag
import hashlib

from .models import SongModel
from .models import SingerModel

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
    

class RefreshList(View):

    unsupport_files = []

    def get(self, request):
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
        
        # 2 遍历所有的文件  
        for song_name in song_list:    
            file_path = path + '/' + song_name
    
            try:
                tag = TinyTag.get(file_path)
                print(f'歌曲={tag.title},歌手={tag.artist},时长={tag.duration} 文件名={song_name}') 

                # 获取文件的MD5 
                file_hash_value = self.checksum(file_path)
                                
                # 文件在数据库中是否已经存在；已存在则跳过，不存在则插入到数据库 
                exist = SongModel.objects.filter(id=file_hash_value).exists()
                
                if not exist:
                    # 歌手是否已经存在
                    self.update_singer(tag)     
                    # 更新歌曲信息
                    self.update_song(tag)                                   
                
            except Exception as e:
                print(f"Error reading audio info: {e} {song_name}")
                self.unsupport_files.append(song_name)
                # 记录未解析文件 
        

    def update_song(self, song_info: TinyTag):
        """
        更新歌曲到数据库
        """
        if song_info.title == None:
            print(f"没有读取到数据文件= {song_name}")
            self.unsupport_files.append(song_name)
        else:
            song_name = song_info.title
            singer = song_info.artist 
            duration = song_info.duration
            

    def update_singer(self, song_info: TinyTag):
        singer = song_info.artist
        SingerModel.objects.filter()
        

    def checksum(self, filename):
        """
        获取大文件的哈希值
        """
        file_hash = hashlib.md5()
        with open(filename, 'rb') as f:
            while chunk := f.read(8192):
                file_hash.update(chunk)
        
        print(file_hash.hexdigest())
        return file_hash.digest()
    
