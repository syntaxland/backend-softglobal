# live_chat/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

ROOM_TOPIC = (
        ('OTP', 'OTP'),
        ('Payments', 'Payments'),
        ('Support', 'Support'),
        ('Services', 'Services'),
        ('Others', 'Others'),
    )


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name='chat_rooms')
    room_topic = models.CharField(max_length=225, null=True, blank=True, choices=ROOM_TOPIC)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.room_name


class RoomMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='chat_message_user')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.message}'
 

class MessageId(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="message_id_user")
    msg_id = models.CharField(max_length=30, unique=True, null=True)
    message = models.TextField(max_length=500, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.msg_id}"


class MessageUser(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="receiver")
    message_id = models.ForeignKey(MessageId, on_delete=models.CASCADE, related_name='message_user_id', blank=True, null=True)
    message = models.TextField(max_length=500, null=True, blank=True)
    sender_msg_count = models.PositiveIntegerField(default=0, editable=False)
    receiver_msg_count = models.PositiveIntegerField(default=0, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self): 
        return f"{self.sender} | {self.receiver} | {self.message}"  
