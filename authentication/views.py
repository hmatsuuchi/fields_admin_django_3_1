from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.conf import settings
from django.middleware import csrf
from authentication.customAuthentication import CustomAuthentication


class LogoutView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([IsAuthenticated])
    
    def post(self, request, format=None):
        try:
            # gets the refresh token from the cookie
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['LOGOUT_COOKIE'])
            # checks if the refresh token is present    
            if refresh_token is None:
                return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
            # blacklists the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            # deletes access cookie
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'], samesite='None')

            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CsrfRefreshView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        response = Response()
        
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

        response.data = {"Success" : "Successfully refreshed token", "csrftoken" : csrf_token_value}

        return response