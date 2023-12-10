from django.urls import path 
from .views import Login, LoginAPI, RefreshList

urlpatterns = [
    path('login', Login.as_view()),
    path('api/login', LoginAPI.as_view()),
    path('api/refresh', RefreshList.as_view())
]