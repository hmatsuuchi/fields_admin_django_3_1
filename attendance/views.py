from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# group permission control
from authentication.permissions import isInStaffGroup
# authentication
from authentication.customAuthentication import CustomAuthentication

# get all attendance records for single date
class AttendanceForDateView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        try:
            # get date parameter from request
            date = request.GET.get('date')

            data = {
                'date from request': date,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)