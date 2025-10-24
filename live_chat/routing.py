# live_chat/routing.py
from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/room-chat/(?P<room_name>\w+)/$', consumers.RoomChatConsumer.as_asgi()), 
    re_path(r'ws/user-chat/(?P<msg_id>\w+)/$', consumers.UserChatConsumer.as_asgi()), 
]
