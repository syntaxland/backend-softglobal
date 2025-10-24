# tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from live_chat.models import ChatRoom, RoomMessage, MessageId, MessageUser

User = get_user_model()

class ChatRoomModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.room = ChatRoom.objects.create(room_name="Test Room", room_topic="Support")

    def test_chat_room_creation(self):
        self.assertEqual(ChatRoom.objects.count(), 1)
        self.assertEqual(self.room.room_name, "Test Room")
        self.assertEqual(self.room.room_topic, "Support")

    def test_add_users_to_room(self):
        self.room.users.add(self.user1, self.user2)
        self.assertEqual(self.room.users.count(), 2)
        self.assertIn(self.user1, self.room.users.all())


class RoomMessageModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password123")
        self.room = ChatRoom.objects.create(room_name="Test Room")
        self.message = RoomMessage.objects.create(room=self.room, user=self.user, message="Test message")

    def test_room_message_creation(self):
        self.assertEqual(RoomMessage.objects.count(), 1)
        self.assertEqual(self.message.room, self.room)
        self.assertEqual(self.message.user, self.user)
        self.assertEqual(self.message.message, "Test message")


class MessageIdModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password123")
        self.message_id = MessageId.objects.create(user=self.user, msg_id="12345", message="Test message")

    def test_message_id_creation(self):
        self.assertEqual(MessageId.objects.count(), 1)
        self.assertEqual(self.message_id.msg_id, "12345")
        self.assertEqual(self.message_id.message, "Test message")


class MessageUserModelTest(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="password123")
        self.receiver = User.objects.create_user(username="receiver", password="password123")
        self.message_id = MessageId.objects.create(user=self.sender, msg_id="67890", message="Test message ID")
        self.message_user = MessageUser.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            message_id=self.message_id,
            message="Hello!"
        )

    def test_message_user_creation(self):
        self.assertEqual(MessageUser.objects.count(), 1)
        self.assertEqual(self.message_user.sender, self.sender)
        self.assertEqual(self.message_user.receiver, self.receiver)
        self.assertEqual(self.message_user.message, "Hello!")


class GetRoomMessagesViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password123")
        self.room = ChatRoom.objects.create(room_name="Test Room")
        RoomMessage.objects.create(room=self.room, user=self.user, message="First message")
        RoomMessage.objects.create(room=self.room, user=self.user, message="Second message")
        self.client.login(username="user", password="password123")

    def test_get_room_messages(self):
        response = self.client.get(f'/get-room-messages/?room_name={self.room.room_name}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


class GetUserMessagesViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password123")
        self.message_id = MessageId.objects.create(user=self.user, msg_id="12345", message="Test message")
        MessageUser.objects.create(sender=self.user, receiver=self.user, message_id=self.message_id, message="Hello!")
        self.client.login(username="user", password="password123")

    def test_get_user_messages(self):
        response = self.client.get(f'/get-user-messages/?msg_id={self.message_id.msg_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message'], "Hello!")
