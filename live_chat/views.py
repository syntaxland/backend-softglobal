# live_chat/views.py
import random
import string

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
 
from .models import RoomMessage, ChatRoom, MessageId, MessageUser 
from .serializers import ChatRoomSerializer, RoomMessageSerializer, MessageUserSerializer 


class GetRoomMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_name):
        try:
            room = ChatRoom.objects.get(room_name=room_name)
            messages = RoomMessage.objects.filter(room=room).order_by('timestamp')
            serializer = RoomMessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ChatRoom.DoesNotExist:
            return Response({'error': 'Room does not exist'}, status=status.HTTP_404_NOT_FOUND)


class GetUserMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, msg_id):
        try:
            message_id = MessageId.objects.get(msg_id=msg_id)
            messages = MessageUser.objects.filter(message_id=message_id).order_by('timestamp')
            serializer = MessageUserSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MessageId.DoesNotExist:
            return Response({'error': 'Message does not exist'}, status=status.HTTP_404_NOT_FOUND)
        

class CreateMessageIdView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        print('data:', data, 'user:', user)

        msg_id = MessageId.objects.filter(user=user).first()
        if not msg_id:
            msg_id = MessageId.objects.create(
                user=user,
                msg_id=generate_message_id(),
            )

        msg_id = MessageId.objects.get(user=user)

        message_id = msg_id.msg_id
        print('message_id:', message_id)

        return Response({'message_id': message_id}, status=status.HTTP_201_CREATED)
     

def generate_message_id():
    return ''.join(random.choices(string.digits, k=20))
