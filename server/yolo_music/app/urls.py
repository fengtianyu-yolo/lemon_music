from django.urls import path 
# from .views import test, TestView, Test2View, Test4View, RefreshList, Songs
# from .views import StreamAudio, StreamView, StreamSegment
# from .search_module.SearchView import Search, SearchArtist
# from .device_transfer.DeviceView import DeviceView
# from .views import MusicScanner  # 添加这行导入语句
# from .views import get_song_list
from .views.music_scanner import MusicScannerView, MusicRefreshView
from .views.query_song import all_songs, unrecognized_files, query_tags, query_tag_songs
from .views.update_song import update_song,add_tag_to_song
from .views.create_tag import create_tag

urlpatterns = [
    # path('test/', test),
    # path('test2/', TestView.as_view()),
    # path('test3/', Test2View.as_view()),
    # path('test4/<str:msg>/<int:id>', Test4View.as_view()),
    # path('refresh', RefreshList.as_view()),
    # path('songs', Songs.as_view()),
    # path('search', Search.as_view()),
    # path('artist', SearchArtist.as_view()),
    # path('stream/<str:filename>', StreamAudio.as_view(), name='stream_audio'),
    # path('stream/<str:filepath>', StreamAudio.as_view(), name='stream_audio'),
    # path('stream', StreamAudio.as_view(), name='stream_audio'),
    # path('stream/<str:filename>/<str:segment>', StreamSegment.as_view(), name='stream_segment'),
    # path('stream/<str:filepath>/<str:segment>', StreamSegment.as_view(), name='stream_segment'),
    # path('segment', StreamSegment.as_view(), name='stream_segment'),
    # path('device', DeviceView.as_view()),
    # path('scan', MusicScanner.as_view()),
    # path('songs/list', get_song_list, name='song_list'),
    path('scan', MusicScannerView.as_view(), name='scan_music'),
    path('refresh', MusicRefreshView.as_view(), name='scan_music'),
    path('songs', all_songs, name='songs'),
    path('unknows', unrecognized_files, name='unrecognized_songs'),
    path('update', update_song, name='update_song'),
    path('tag/create', create_tag, name='create_tag'),
    path('tags', query_tags, name='create_tag'),
    path('song/addtag', add_tag_to_song, name='add_tag'),
    path('tag/songlist', query_tag_songs, name='tag_songs'),
]