from django.urls import path 
from .views import Login, LoginAPI, RefreshList, SongList, Search, Dashboard, Test

urlpatterns = [
    path('login', Login.as_view()),
    path('api/login', LoginAPI.as_view()),
    path('api/refresh', RefreshList.as_view()),
    path('api/songs', SongList.as_view()),
    path('api/search', Search.as_view()),
    path('api/dashboard', Dashboard.as_view()),
    path('test', Test.as_view())
]