# live_chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get-room-messages/', views.GetRoomMessagesView.as_view(), name='get-room-messages'),
    path('get-user-messages/', views.GetUserMessagesView.as_view(), name='get-user-messages'),
    path('create-message-id/', views.CreateMessageIdView.as_view(), name='create-message-id'),
]
