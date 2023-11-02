from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, format=None):
        try:
            print("logout successful")
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print("logout error")
            return Response(status=status.HTTP_400_BAD_REQUEST)