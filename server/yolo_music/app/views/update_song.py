from django.http import JsonResponse
import json
from ..models import Song, Artist
import re

def update_song(request):
    """
    更新或创建歌曲信息的视图函数
    """
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    try:
        data = json.loads(request.body)
        title = data.get('title')
        artists_field = data.get('artists')

        if not title or not artists_field:
            return JsonResponse({"error": "title和artists字段必填"}, status=400)

        # 分割artists字段
        artist_names = [a.strip() for a in re.split(r"[、&/]", artists_field) if a.strip()]

        # 查询是否有该title的歌曲
        songs = Song.objects.filter(title=title)
        for song in songs:
            db_artist_names = list(song.artists.values_list('name', flat=True))
            if sorted(db_artist_names) == sorted(artist_names):
                return JsonResponse({"success": True, "message": "该歌曲已存在"})

        # 不存在则创建
        song = Song.objects.create(title=title)
        for artist_name in artist_names:
            artist, _ = Artist.objects.get_or_create(name=artist_name)
            song.artists.add(artist)
        song.save()

        return JsonResponse({"success": True, "message": "Song created successfully."})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)