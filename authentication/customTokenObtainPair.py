from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf

from datetime import datetime

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# this class is used to perform the initial username and password authentication
# and if the authentication is successful, it sets access and refresh cookies and passes the csrf token in the response
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, format=None):
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)

                # access token is set as a cookie
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value = data["access"],
                    expires = datetime.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )

                # refresh token is set as a cookie
                response.set_cookie(
                    key = settings.SIMPLE_JWT['REFRESH_COOKIE'],
                    value = data["refresh"],
                    expires = datetime.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['REFRESH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['REFRESH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['REFRESH_COOKIE_SAMESITE'],
                    path = settings.SIMPLE_JWT['REFRESH_COOKIE_PATH'],
                )

                # logout token (refresh token) is set as a cookie
                response.set_cookie(
                    key = settings.SIMPLE_JWT['LOGOUT_COOKIE'],
                    value = data["refresh"],
                    expires = datetime.now() + settings.SIMPLE_JWT['LOGOUT_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['LOGOUT_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['LOGOUT_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['LOGOUT_COOKIE_SAMESITE'],
                    path = settings.SIMPLE_JWT['LOGOUT_COOKIE_PATH'],
                )

                # generate csrf token
                csrf_token_value = csrf.get_token(request)

                # csrf token is set as a cookie
                response.set_cookie(
                    key = settings.CSRF_COOKIE,
                    value = csrf_token_value,
                    secure = settings.CSRF_COOKIE_SECURE,
                    httponly = settings.CSRF_COOKIE_HTTPONLY,
                    samesite = settings.CSRF_COOKIE_SAMESITE,
                )

                response.data = {"Success" : "Successfully logged in", "csrftoken" : csrf_token_value}

                return response
            else:
                return Response({"No active" : "This account is not active"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password"}, status=status.HTTP_404_NOT_FOUND)
        
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # get refresh token from cookie
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_COOKIE'])
        if refresh_token is None:
            return Response({"error": "No refresh token found in cookie"}, status=status.HTTP_400_BAD_REQUEST)
                
        # set refresh token in request data
        request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)

        new_refresh_token = response.data['refresh']
        new_access_token = response.data['access']

        # new access token is set as a cookie
        response.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_COOKIE'],
            value = new_access_token,
            expires = datetime.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )
        
        # new refresh token is set as a cookie
        response.set_cookie(
            key = settings.SIMPLE_JWT['REFRESH_COOKIE'],
            value = new_refresh_token,
            expires = datetime.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['REFRESH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['REFRESH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['REFRESH_COOKIE_SAMESITE'],
            path = settings.SIMPLE_JWT['REFRESH_COOKIE_PATH'],
        )

        # new logout token is set as a cookie
        response.set_cookie(
            key = settings.SIMPLE_JWT['LOGOUT_COOKIE'],
            value = new_refresh_token,
            expires = datetime.now() + settings.SIMPLE_JWT['LOGOUT_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['LOGOUT_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['LOGOUT_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['LOGOUT_COOKIE_SAMESITE'],
            path = settings.SIMPLE_JWT['LOGOUT_COOKIE_PATH'],
        )

        response.data = {"Success" : "Successfully refreshed token"}

        return response