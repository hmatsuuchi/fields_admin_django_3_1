from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoggedInUserDataSerializer

class LoggedInUserDataView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        try:
            logged_in_user = request.user
            serializer = LoggedInUserDataSerializer(logged_in_user)
            group_names = serializer.get_groups(logged_in_user)

            response_data = {
                'logged_in_user_data': serializer.data,
                'logged_in_user_groups': group_names,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)