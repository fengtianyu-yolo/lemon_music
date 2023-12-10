from django.urls import path 
from .views import Login, LoginAPI, RefreshList, SongList

urlpatterns = [
    path('login', Login.as_view()),
    path('api/login', LoginAPI.as_view()),
    path('api/refresh', RefreshList.as_view()),
    path('api/songs', SongList.as_view())
]