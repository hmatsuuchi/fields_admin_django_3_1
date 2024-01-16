from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    # valid users CAN log in and obtain access and refresh tokens
    def test_login_valid_user(self):
        user = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(reverse('token_obtain_pair'), user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['access']), 0)
        self.assertGreater(len(response.data['refresh']), 0)

    # invalid users CANNOT log in and obtain access and refresh tokens
    def test_login_invalid_user(self):
        user = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

        response = self.client.post(reverse('token_obtain_pair'), user)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # valid users CAN log in and refresh access and refresh tokens
    def test_token_refresh_valid_user(self):
        user = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(reverse('token_obtain_pair'), user)
        old_access_token = response.data['access']
        old_refresh_token = response.data['refresh']

        refresh = {
            'refresh': old_refresh_token
        }

        response = self.client.post(reverse('token_refresh'), refresh)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['access']), 0)
        self.assertGreater(len(response.data['refresh']), 0)
        self.assertNotEqual(old_access_token, response.data['access'])
        self.assertNotEqual(old_refresh_token, response.data['refresh'])

    # invalid users CANNOT refresh access and refresh tokens
    def test_token_refresh_invalid_user(self):
        refresh = {
            'refresh': 'wrongtoken'
        }

        response = self.client.post(reverse('token_refresh'), refresh)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # valid users CAN log out
    def test_logout_valid_user(self):
        user = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(reverse('token_obtain_pair'), user)
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        refresh = {
            'refresh_token': refresh_token
        }

        response = self.client.post(reverse('logout'), refresh, HTTP_AUTHORIZATION='Bearer ' + access_token)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        response = self.client.post(reverse('token_refresh'), refresh)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # invalid users CANNOT log out
    def test_logout_invalid_user(self):
        refresh_token = 'wrongrefresh'
        access_token = 'wrongaccess'

        refresh = {
            'refresh_token': refresh_token
        }

        response = self.client.post(reverse('logout'), refresh, HTTP_AUTHORIZATION='Bearer ' + access_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)