# live_chat/consumers.py
import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import RoomMessage, ChatRoom, MessageId, MessageUser
from django.conf import settings
from django.apps import apps

User = apps.get_model(settings.AUTH_USER_MODEL) 

class RoomChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def save_message(self, room_name, user, message):
        room = ChatRoom.objects.get(room_name=room_name)
        return RoomMessage.objects.create(room=room, user=user, message=message)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        room_name = text_data_json['room_name']  
        timestamp = text_data_json['timestamp']  

        sender = await database_sync_to_async(User.objects.get)(id=sender_id)

        # Save the message
        await self.save_message(room_name, sender, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.first_name,
                'room_name': room_name,  
                'timestamp': timestamp, 
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        room_name = event['room_name']  
        timestamp = event['timestamp']  

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'room_name': room_name,  
            'timestamp': timestamp,  
        }))


class UserChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.msg_id = self.scope['url_route']['kwargs'].get('msg_id')
        self.room_group_name = f'chat_{self.msg_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        receiver_id = text_data_json['receiver_id']
        timestamp = text_data_json['timestamp']

        try:
            sender = await database_sync_to_async(User.objects.get)(id=sender_id)
            receiver = await database_sync_to_async(User.objects.get)(id=receiver_id)

            message_instance = await self.save_message(sender, receiver, self.msg_id, message, timestamp)

            if not message_instance:
                return  # Exit if saving the message failed

            # Send message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.first_name,
                    'receiver': receiver.first_name,
                    'msg_id': self.msg_id,
                    'timestamp': timestamp,
                }
            )
        except Exception as e:
            print(f"Error in receive method: {e}")

    async def save_message(self, sender, receiver, msg_id, message, timestamp):
        try:
            message_id = await database_sync_to_async(MessageId.objects.get)(msg_id=msg_id)

            message_instance = await database_sync_to_async(MessageUser.objects.create)(
                sender=sender,
                receiver=receiver,
                message_id=message_id,
                message=message,
                timestamp=timestamp,
            )

            # Update sender and receiver message counts
            message_id.user = sender
            message_id.message = message
            message_id.timestamp = timezone.now()
            await database_sync_to_async(message_id.save)()

            # Update message counts in MessageUser
            await database_sync_to_async(self.update_message_counts)(message_id, sender, receiver)

            return message_instance
        except Exception as e:
            print(f"Error saving message: {e}")
            return None

    def update_message_counts(self, message_id, sender, receiver):
        message_users = MessageUser.objects.filter(message_id=message_id)
        sender_messages = message_users.filter(sender=sender).count()
        receiver_messages = message_users.filter(receiver=receiver).count()

        for message_user in message_users:
            if message_user.sender == sender:
                message_user.sender_msg_count = sender_messages
            if message_user.receiver == receiver:
                message_user.receiver_msg_count = receiver_messages
            message_user.save()

    async def chat_message(self, event):
        # Receive message from room group
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        msg_id = event['msg_id']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver,
            'msg_id': msg_id,
            'timestamp': timestamp,
        }))
