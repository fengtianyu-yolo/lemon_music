# views.py
from django.http import JsonResponse
from urllib.parse import parse_qs, unquote
from ..models import Song
from ..models import UnmatchedMusic
from ..models import Tag


def all_songs(request):
    """
    查询所有歌曲及相关信息，并以 JSON 返回
    """
    data = []

    # 使用 prefetch_related 减少查询次数
    songs = Song.objects.prefetch_related('artists', 'audiofile_set', 'tags').all()
    
    for song in songs:
        song_data = {
            "id": song.id,
            "title": song.title,
            "cover": song.cover.url if song.cover else None,
            "duration": song.duration,
            "artists": [artist.name for artist in song.artists.all()],
            "play_count": song.play_count,
            "update_time": song.updated_at,
            "audio_files": [
                {
                    "file": audio.file,
                    "quality": audio.quality
                } for audio in song.audiofile_set.all()
            ],
            "tags": [
                {"id": tag.id, "name": tag.name}
                for tag in song.tags.all()
            ]  # 标签内容携带id和name
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
    dataList = [{"filename": f.file_name, "file_path": f.file_path, "text1": f.elem1, "text2": f.elem2} for f in unrecognized_songs]
    response = {
        "data": dataList
    }

    return JsonResponse(response, safe=False)

def query_tags(request):
    """
    查询所有标签，并以 JSON 返回
    """
    tags = Tag.objects.all()
    tag_list = [{"id": tag.id, "name": tag.name} for tag in tags]
    return JsonResponse({"data": tag_list}, safe=False)

def query_tag_songs(request):
    """
    查询某个标签下的所有歌曲，并以 JSON 返回
    """
    try:
        body = request.body.decode('utf-8')
        params = parse_qs(body)
        tag_id = unquote(params.get('tag_id', [''])[0])
        tag = Tag.objects.get(id=tag_id)
        songs = tag.songs.prefetch_related('artists', 'audiofile_set').all()
        
        data = []
        for song in songs:
            song_data = {
                "id": song.id,
                "title": song.title,
                "cover": song.cover.url if song.cover else None,
                "duration": song.duration,
                "artists": [artist.name for artist in song.artists.all()],
                "play_count": song.play_count,
                "update_time": song.updated_at,
                "audio_files": [
                    {
                        "file": audio.file,
                        "quality": audio.quality
                    } for audio in song.audiofile_set.all()
                ],
                "tags": [
                    {"id": tag.id, "name": tag.name}
                    for tag in song.tags.all()
                ]  # 标签内容携带id和name
            }
            data.append(song_data)
        
        response = {
            "data": data
        }
        return JsonResponse(response, safe=False)
    except Tag.DoesNotExist:
        return JsonResponse({"error": "Tag not found"}, status=404)