from django.urls import path 
from .views import test, TestView, Test2View, Test4View, RefreshList, Songs
from .search_module.SearchView import Search, SearchArtist

urlpatterns = [
    path('test/', test),
    path('test2/', TestView.as_view()),
    path('test3/', Test2View.as_view()),
    path('test4/<str:msg>/<int:id>', Test4View.as_view()),
    path('refresh', RefreshList.as_view()),
    path('songs', Songs.as_view()),
    path('search', Search.as_view()),
    path('artist', SearchArtist.as_view())
]