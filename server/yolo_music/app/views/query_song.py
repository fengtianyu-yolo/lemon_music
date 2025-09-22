# views.py
from django.http import JsonResponse
from ..models import Song

def all_songs(request):
    """
    查询所有歌曲及相关信息，并以 JSON 返回
    """
    data = []

    # 使用 prefetch_related 减少查询次数
    songs = Song.objects.prefetch_related('artists', 'audiofile_set').all()

    for song in songs:
        song_data = {
            "title": song.title,
            "cover": song.cover.url if song.cover else None,  # 封面路径
            "duration": song.duration,
            "artists": [artist.name for artist in song.artists.all()],
            "audio_files": [
                {
                    "file": audio.file,
                    "quality": audio.quality
                } for audio in song.audiofile_set.all()
            ]
        }
        data.append(song_data)

    return JsonResponse(data, safe=False)
