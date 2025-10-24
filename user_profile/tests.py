# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user_profile.models import User
from django.urls import reverse


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'password123',
            'phone_number': '1234567890',
        }

    def test_create_user(self):
        user = User.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            password=self.user_data['password'],
            phone_number=self.user_data['phone_number'],
        )
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.email, self.user_data['email'])

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            username='adminuser',
            password='adminpassword',
            phone_number='0987654321',
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_email_is_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=None, username='user', password='password123'
            )

    def test_string_representation(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])


class UserRegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user-register') 
        self.user_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'password123',
            'phone_number': '1234567890',
        }

    def test_register_user_successfully(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('detail', response.data)

    def test_register_existing_email(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

    def test_register_with_invalid_data(self):
        invalid_data = {**self.user_data, 'email': ''}
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123',
            phone_number='1234567890',
        )
        self.client.force_authenticate(user=self.user)
        self.logout_url = reverse('user-logout')

    def test_logout_successfully(self):
        refresh_token = str(self.client.post(reverse('token_obtain_pair'), {
            'email': self.user.email,
            'password': 'password123'
        }).data['refresh'])
        response = self.client.post(self.logout_url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_with_invalid_token(self):
        response = self.client.post(self.logout_url, {'refresh': 'invalid_token'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class ChangePasswordViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='oldpassword123',
            phone_number='1234567890',
        )
        self.client.force_authenticate(user=self.user)
        self.change_password_url = reverse('change-password')  

    def test_change_password_successfully(self):
        response = self.client.post(self.change_password_url, {
            'old_password': 'oldpassword123',
            'new_password': 'newpassword456',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)

    def test_change_password_with_incorrect_old_password(self):
        response = self.client.post(self.change_password_url, {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword456',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

    def test_change_password_with_invalid_data(self):
        response = self.client.post(self.change_password_url, {
            'old_password': '',
            'new_password': 'newpassword456',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old_password', response.data)

class GetUserProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123',
            phone_number='1234567890',
        )
        self.client.force_authenticate(user=self.user)
        self.profile_url = reverse('get-user-profile') 

    def test_get_user_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)

