from django.urls import path 
from .views import Login, LoginAPI

urlpatterns = [
    path('login', Login.as_view()),
    path('api/login', LoginAPI.as_view())
]