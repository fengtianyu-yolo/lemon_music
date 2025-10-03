# views.py
from django.http import JsonResponse
from ..models import Song
from ..models import UnmatchedMusic

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
            "play_count": song.play_count,
            "update_time": song.updated_at,
            "audio_files": [
                {
                    "file": audio.file,
                    "quality": audio.quality
                } for audio in song.audiofile_set.all()
            ]
        }
        data.append(song_data)
    response = {
        "data": data
    }
    return JsonResponse(response, safe=False)

def unrecognized_files(request):
    """
    查询所有未识别的文件，并以 JSON 返回
    """

    unrecognized_songs = UnmatchedMusic.objects.all()
    data = [{"file_path": f.file_path, "text1": f.elem1, "text2": f.elem2} for f in unrecognized_songs]

    return JsonResponse(data, safe=False)