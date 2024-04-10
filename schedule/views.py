from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
# group permission control
from authentication.permissions import isInStaffGroup
# authentication
from authentication.customAuthentication import CustomAuthentication
# models
from .models import Events
from django.contrib.auth.models import User
# serializers
from .serializers import EventsSerializer, InstructorSerializer

# get all events for single date
class EventsAllView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        try:
            # get all events for date
            events = Events.objects.all().order_by('day_of_week', 'start_time')
            
            # serialize events
            event_serializer = EventsSerializer(events, many=True)

            # get all instructors for events
            instructors = User.objects.filter(events__in=events).distinct().order_by('username')

            # serialize instructors
            instructor_serializer = InstructorSerializer(instructors, many=True)

            data = {
                'events': event_serializer.data,
                'instructors': instructor_serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)