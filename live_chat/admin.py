# live_chat/admin.py
from django.contrib import admin
from . import models


@admin.register(models.ChatRoom)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'id', 'created_at', )  
    search_fields = ('room_name',) 


@admin.register(models.RoomMessage)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'message', 'timestamp',  )  


@admin.register(models.MessageId)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'msg_id', 'timestamp',)  


@admin.register(models.MessageUser)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'receiver', 'message', 'timestamp',)  
