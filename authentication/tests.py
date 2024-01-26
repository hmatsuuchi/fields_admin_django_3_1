from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# tests JWT authentication endpoints
class AuthenticationTest(TestCase):
    def setUp(self):
        # setup test client
        self.client = Client()
        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    # valid users CAN log in and obtain access, refresh, logout and csrf tokens
    def test_login_valid_user(self):
        user = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        # attempt to log in and obtain access, refresh, logout and csrf tokens
        response = self.client.post(reverse('token_obtain_pair'), user)

        # assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']].value), 0)
        self.assertGreater(len(response.cookies[settings.SIMPLE_JWT['REFRESH_COOKIE']].value), 0)
        self.assertGreater(len(response.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']].value), 0)
        self.assertGreater(len(response.cookies['csrftoken'].value), 0)

    # invalid users CANNOT log in and obtain access and refresh tokens
    def test_login_invalid_user(self):
        user = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

        # attempt to log in and obtain access, refresh, logout and csrf tokens
        response = self.client.post(reverse('token_obtain_pair'), user)

        # assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # users with valid refresh tokens CAN refresh access, refresh and logout tokens
    def test_token_refresh_valid_user(self):
        # get test user
        user = User.objects.get(username='testuser')

        # generate access and refresh token
        first_stage_refresh_token = RefreshToken.for_user(user)
        first_stage_access_token = AccessToken.for_user(user)
        first_stage_logout_token = first_stage_refresh_token

        # set access and refresh token in cookie
        self.client.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']] = str(first_stage_access_token)
        self.client.cookies[settings.SIMPLE_JWT['REFRESH_COOKIE']] = str(first_stage_refresh_token)
        self.client.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']] = str(first_stage_logout_token)

        # attempt to refresh token
        response = self.client.post(reverse('token_refresh'), content_type='application/json')

        # get new access and refresh token
        second_stage_access_token = self.client.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']].value
        second_stage_refresh_token = self.client.cookies[settings.SIMPLE_JWT['REFRESH_COOKIE']].value
        second_stage_logout_token = self.client.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']].value

        # set new access and new refresh token in cookie
        self.client.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']] = str(second_stage_access_token)
        self.client.cookies[settings.SIMPLE_JWT['REFRESH_COOKIE']] = str(second_stage_refresh_token)
        self.client.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']] = str(second_stage_logout_token)

        # attempt to refresh token
        response = self.client.post(reverse('token_refresh'), content_type='application/json')

        # assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(second_stage_access_token), 0)
        self.assertGreater(len(second_stage_refresh_token), 0)
        self.assertGreater(len(second_stage_logout_token), 0)
        self.assertNotEqual(second_stage_access_token, response.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']].value)
        self.assertNotEqual(second_stage_refresh_token, response.cookies[settings.SIMPLE_JWT['REFRESH_COOKIE']].value)
        self.assertNotEqual(second_stage_logout_token, response.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']].value)

    # users with blacklist refresh tokens CANNOT refresh access and refresh tokens
    def test_token_refresh_invalid_user(self):
        # get test user
        user = User.objects.get(username='testuser')

        # generate access and refresh token
        old_access_token = AccessToken.for_user(user)
        old_refresh_token = RefreshToken.for_user(user)
        old_logout_token = old_refresh_token

        # set access and refresh token in cookie
        self.client.cookies[settings.SIMPLE_JWT['REFRESH_COOKIE']] = str(old_refresh_token)
        self.client.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']] = str(old_access_token)
        self.client.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']] = str(old_logout_token)

        # attempt to refresh token
        response = self.client.post(reverse('token_refresh'), content_type='application/json')

        # get new access, refresh and logout tokens from cookies
        new_access_token = response.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']].value
        new_refresh_token = response.cookies[settings.SIMPLE_JWT['REFRESH_COOKIE']].value
        new_logout_token = response.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']].value

        # se newt access, refresh and logout tokens in cookie
        self.client.cookies[settings.SIMPLE_JWT['REFRESH_COOKIE']] = str(old_refresh_token)
        self.client.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']] = str(new_access_token)
        self.client.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']] = str(new_logout_token)

        # attempt to refresh token with blacklisted refresh token
        response = self.client.post(reverse('token_refresh'), content_type='application/json')

        # assertions
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # users with valid refresh tokens CAN log out
    def test_logout_valid_user(self):
        # get test user
        user = User.objects.get(username='testuser')

        # generate access, refresh and logout tokens
        refresh_token = RefreshToken.for_user(user)
        access_token = AccessToken.for_user(user)
        logout_token = refresh_token

        # set access, refresh and logout tokens in cookies
        self.client.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']] = str(access_token)
        self.client.cookies[settings.SIMPLE_JWT['REFRESH_COOKIE']] = str(refresh_token)
        self.client.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']] = str(logout_token)

        # attempt to log out
        response = self.client.post(reverse('logout'), content_type='application/json')

        # assertion
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

        # attempt to obtain new access token with expired refresh token
        response = self.client.post(reverse('token_refresh'), content_type='application/json')

        #assertion
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # users with blacklisted refresh tokens CANNOT log out
    def test_logout_invalid_user(self):
        # get test user
        user = User.objects.get(username='testuser')

        # generate access and refresh token
        old_access_token = AccessToken.for_user(user)
        old_refresh_token = RefreshToken.for_user(user)
        old_logout_token = old_refresh_token

        # set access and refresh token in cookie
        self.client.cookies[settings.SIMPLE_JWT['REFRESH_COOKIE']] = str(old_refresh_token)
        self.client.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']] = str(old_access_token)
        self.client.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']] = str(old_logout_token)

        # attempt to refresh token
        response = self.client.post(reverse('token_refresh'), content_type='application/json')

        # get new access, refresh and logout tokens from cookies
        new_access_token = response.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']].value
        new_refresh_token = response.cookies[settings.SIMPLE_JWT['REFRESH_COOKIE']].value
        new_logout_token = response.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']].value

        # set access, refresh and logout tokens in cookies
        self.client.cookies[settings.SIMPLE_JWT['REFRESH_COOKIE']] = str(new_refresh_token)
        self.client.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']] = str(new_access_token)
        self.client.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']] = str(old_logout_token)

        # attempt to log out with blacklisted refresh token
        response = self.client.post(reverse('logout'), content_type='application/json')

        # assertion
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)