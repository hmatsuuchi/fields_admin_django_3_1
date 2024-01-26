from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# group permission control
from authentication.permissions import isInStaffGroup
# authentication
from authentication.customAuthentication import CustomAuthentication
# models
from .models import Events
# serializers
from .serializers import EventsSerializer

# get all events
class EventsForDateRangeListView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])
    
    def get(self, request, format=None):
        try:
            events = Events.objects.all()
            serializer = EventsSerializer(events, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

            
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)