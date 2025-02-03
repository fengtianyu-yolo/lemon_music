from django.views import View
from django.http import JsonResponse
from app.models import DeviceSongsModel, DeviceModel, SongModel
from django.views.decorators.csrf import csrf_exempt
import json

# @csrf_exempt
class DeviceView(View):
    def get(self, request):
        """获取设备的所有歌曲数据"""
        # 获取请求参数device_id
        device_id = request.GET.get('device_id')
        
        if not device_id:
            return JsonResponse({
                'code': 400,
                'message': '缺少device_id参数'
            }, status=400)
        
        try:
            # 查询设备的所有歌曲数据
            device_songs = DeviceSongsModel.objects.filter(device_id=device_id)
            
            # 将查询结果转换为字典列表
            songs_list = []
            for song in device_songs:
                songs_list.append(song.song_id)
            
            return JsonResponse({
                'code': 200,
                'message': '获取成功',
                'data': songs_list
            })
            
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'message': f'服务器错误: {str(e)}'
            }, status=500)
    
    # @csrf_exempt
    def post(self, request):
        """添加设备的歌曲数据"""
        # 获取请求参数
        requestData = json.loads(request.body)
        device_id = requestData.get('device_id')
        song_ids = requestData.get('song_ids')
        print(song_ids)
        print(device_id)
        if not device_id or not song_ids:
            return JsonResponse({
                'code': 400,
                'message': '缺少必要参数'
            }, status=200)

        try:
            if not DeviceModel.objects.filter(device_id=device_id).exists():
                # 创建新的设备对象
                device = DeviceModel()
                device.device_id = device_id
                device.save()
            else:
                # 获取已存在的设备对象
                device = DeviceModel.objects.get(device_id=device_id)
            
            # 遍历歌曲列表，添加歌曲数据
            for song_id in song_ids:
                # 获取歌曲对象
                song = SongModel.objects.get(song_id=song_id)
                # 创建新的设备歌曲数据对象
                device_song = DeviceSongsModel()
                device_song.device = device
                device_song.song = song
                device_song.save()
            return JsonResponse({
                'code': 200,
               'message': '添加成功'
            })
                      
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'message': f'服务器错误: {str(e)}'
            }, status=500)
    
    
    def put(self, request):
        """更新设备的歌曲数据"""
        # 获取请求参数
        device_id = request.PUT.get('device_id')
        song_id = request.PUT.get('song_id')
        song_name = request.PUT.get('song_name')
        if not device_id or not song_id or not song_name:
            return JsonResponse({
                'code': 400,
                'message': '缺少必要参数'
            }, status=400)
        try:
            # 查询设备歌曲数据对象
            device_song = DeviceSongsModel.objects.get(device_id=device_id, song_id=song_id)
            # 更新歌曲名称
            device_song.song_name = song_name
            device_song.save()
            return JsonResponse({
                'code': 200,
                'message': '更新成功'
            })
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'message': f'服务器错误: {str(e)}'
            }, status=500)
    
    def delete(self, request):
        """删除设备的歌曲数据"""
        # 获取请求参数
        device_id = request.DELETE.get('device_id')
        song_id = request.DELETE.get('song_id')
        if not device_id or not song_id:
            return JsonResponse({
                'code': 400,
                'message': '缺少必要参数'
            }, status=400)
        try:
            # 查询设备歌曲数据对象
            device_song = DeviceSongsModel.objects.get(device_id=device_id, song_id=song_id)
            # 删除设备歌曲数据对象
            device_song.delete()
            return JsonResponse({
                'code': 200,
                'message': '删除成功'
            })
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'message': f'服务器错误: {str(e)}'
            }, status=500)

