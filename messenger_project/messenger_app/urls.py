from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('chat/', chat, name='chat'),
    path('chat_with/<str:user_name>', chat_with, name='chat_with'),
    path('search-users/', search_users, name='search_users'),
]
