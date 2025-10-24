# live_chat/serializers.py
from rest_framework import serializers
from .models import ChatRoom, RoomMessage, MessageUser


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom 
        fields = '__all__' 


class RoomMessageSerializer(serializers.ModelSerializer): 
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    room_name = serializers.CharField(source='room.room_name', read_only=True)
    class Meta:
        model = RoomMessage
        fields = '__all__'


class MessageUserSerializer(serializers.ModelSerializer): 
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    message_id = serializers.CharField(source='message_id.msg_id', read_only=True)
    class Meta:
        model = MessageUser
        fields = '__all__'