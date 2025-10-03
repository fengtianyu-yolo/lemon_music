from django.http import JsonResponse
from urllib.parse import parse_qs, unquote
import json
from ..models import Song, Artist, AudioFile, UnmatchedMusic
import re
from mutagen import File
from pathlib import Path

def update_song(request):
    """
    更新或创建歌曲信息的视图函数
    """
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    try:
        # data = json.loads(request.body.decode('utf-8'))
        # title = data.get('title')
        # artists_field = data.get('artists')
        # filepath = data.get('filepath') 
        body = request.body.decode('utf-8')
        params = parse_qs(body)
        title = unquote(params.get('title', [''])[0])
        artists_field = unquote(params.get('artists', [''])[0])
        filepath = unquote(params.get('filepath', [''])[0])
        # 获取filepath的后缀 
        f = Path(filepath)

        if not title or not artists_field:
            return JsonResponse({"error": "title和artists字段必填"}, status=400)

        # 分割artists字段
        artist_names = [a.strip() for a in re.split(r"[、&/]", artists_field) if a.strip()]
        # 把artist_names转成set以去重
        artist_names_set = set(artist_names)

        # 查询是否有该title的歌曲
        songs = Song.objects.filter(title=title)
        for song in songs:
            # 检查是否是同一个歌手唱的
            db_artist_names = list(song.artists.values_list('name', flat=True))
            db_artist_names_set = set(db_artist_names)
            # 比较两个集合是否相等 
            if db_artist_names_set == artist_names_set:
                # 检查是否已有该音频文件
                existing_file = AudioFile.objects.filter(song=song, file=filepath).first()
                if not existing_file:
                    quality = "SQ"
                    if f.suffix.lower() == ".mp3":
                        quality = "HQ" 
                    
                    AudioFile.objects.create(
                        song=song, 
                        file=filepath,
                        quality=quality,
                        size=f.stat().st_size
                    )           
                    song.save()
                    return JsonResponse({"success": True, "message": "更新歌曲成功，添加了新的音频文件"})
                else:
                    return JsonResponse({"success": True, "message": "该歌曲已存在"})

        audio = File(filepath)
        duration = int(audio.info.length)  # 单位：秒
        
        # 不存在则创建        
        song = Song.objects.create(title=title)
        song.duration = duration
        for artist_name in artist_names:
            artist, _ = Artist.objects.get_or_create(name=artist_name)
            song.artists.add(artist)
        song.save()

        quality = "SQ"
        if f.suffix.lower() == "mp3":
            quality = "HQ" 
        
        AudioFile.objects.get_or_create(
            song=song, 
            file=filepath,
            defaults={
                "quality": quality,
                "size": f.stat().st_size
            }
        )           
        song.save()
        
        unmatched = UnmatchedMusic.objects.filter(file_path=filepath).first()
        if unmatched:
            unmatched.delete()
        return JsonResponse({"success": True, "message": "歌曲创建成功"})
    except Exception as e:
        print("更新或创建歌曲失败:", e)
        return JsonResponse({"error": str(e)}, status=500)