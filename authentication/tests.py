from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# ======= Authentication Tests =======

# valid users CAN log in and obtain access, refresh, logout and csrf tokens
class LoginAsValidUserTest(TestCase):
    def setUp(self):
        # setup test client
        self.client = Client()
        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

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
        self.assertGreater(len(response.cookies[settings.CSRF_COOKIE].value), 0)
        self.assertGreater(len(response.cookies['csrftoken'].value), 0)

# invalid users CANNOT log in and obtain access, refresh, logout and csrf tokens
class LoginAsInvalidUserTest(TestCase):
    def setUp(self):
        # setup test client
        self.client = Client()
        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_invalid_user(self):
        user = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

        # attempt to log in and obtain access, refresh, logout and csrf tokens
        response = self.client.post(reverse('token_obtain_pair'), user)

        # assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# users with valid refresh tokens CAN refresh access, refresh, logout and csrf tokens
class RefreshAsValidUserTest(TestCase):
    def setUp(self):
        # setup test client
        self.client = Client()
        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

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

# users with blacklist refresh tokens CANNOT refresh access, refresh, logout and csrf tokens
class RefreshWithBlacklistedRefreshTokenTest(TestCase):
    def setUp(self):
        # setup test client
        self.client = Client()
        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

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

# NOT authenticated users CANNOT log out
class LogoutAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logout_unauthenticated_user(self):
        response = self.client.post(reverse('logout'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users with invalid tokens CANNOT log out
class LogoutWithInvalidTokenTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_logout_with_malformed_token(self):
        # Set an invalid token in the logout cookie
        self.client.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']] = 'invalid.token.here'
        
        response = self.client.post(reverse('logout'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users with valid refresh tokens CAN log out
class LogoutWithValidRefreshTokenTest(TestCase):
    def setUp(self):
        # setup test client
        self.client = Client()
        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

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
class LogoutWithBlacklistedRefreshTokenTest(TestCase):
    def setUp(self):
        # setup test client
        self.client = Client()
        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

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

# users with valid refresh tokens CAN log out and delete auth cookie
class LogoutDeletesAuthCookieTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_logout_deletes_auth_cookie(self):
        refresh_token = RefreshToken.for_user(self.user)
        access_token = AccessToken.for_user(self.user)
        
        self.client.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']] = str(access_token)
        self.client.cookies[settings.SIMPLE_JWT['LOGOUT_COOKIE']] = str(refresh_token)

        response = self.client.post(reverse('logout'), content_type='application/json')

        # Verify auth cookie is deleted
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertIn(settings.SIMPLE_JWT['AUTH_COOKIE'], response.cookies)
        self.assertEqual(response.cookies[settings.SIMPLE_JWT['AUTH_COOKIE']].value, '')

# ======= CSRF Refresh Tests =======

# authenticated users CAN refresh csrf token
class CsrfRefreshViewAsAuthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # set test user as authenticated
        self.client.force_authenticate(user=self.user)

    def test_refresh_csrf_token(self):
        # get refresh token
        response = self.client.get(reverse('csrf_refresh'))

        # get new csrf token
        csrf_token = response.cookies[settings.CSRF_COOKIE].value

        # attempt to refresh csrf token
        response = self.client.get(reverse('csrf_refresh'))

        # assertion
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(csrf_token, response.cookies[settings.CSRF_COOKIE].value)

# NOT authenticated users CANNOT refresh csrf token
class CsrfRefreshViewAsUnauthenticatedUserTest(TestCase):
    def test_refresh_csrf_token(self):
        # get refresh token
        response = self.client.get(reverse('csrf_refresh'))

        # assertion
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class CsrfRefreshWithInvalidAuthTest(TestCase):
    def test_csrf_refresh_with_expired_token(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Manually set an invalid/expired token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid.expired.token')
        
        response = self.client.get(reverse('csrf_refresh'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class CsrfRefreshResponseValidationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_csrf_refresh_response_contains_token(self):
        response = self.client.get(reverse('csrf_refresh'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('csrftoken', response.data)
        self.assertGreater(len(response.data['csrftoken']), 0)
