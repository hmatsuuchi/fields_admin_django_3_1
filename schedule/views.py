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
class EventsForSingleDateListView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        try:
            # get date from query params
            request_date = request.GET.get('date')
            date_object = datetime.strptime(request_date, '%Y-%m-%d')

            # get all events for date
            events = Events.objects.all().filter(
                Q(start_date__lte = request_date) &
                Q(end_date__gte = request_date) & Q(day_of_week = date_object.weekday())
                ).order_by('start_time')
            
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

# get all events for date range
class EventsForDateRangeListView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])
    
    def get(self, request, format=None):
        try:
            # get start and end date from query params
            request_start_date = request.GET.get('start_date')
            request_end_date = request.GET.get('end_date')
            date_range = (request_start_date, request_end_date)

            # get all events within date range
            events = Events.objects.all().filter(
                Q(start_date__range = date_range) |
                Q(end_date__range = date_range) |
                Q(start_date__lt = request_start_date, end_date__gte = request_start_date) |
                Q(end_date__gt = request_end_date, start_date__lte = request_end_date)
                ).order_by('start_time')

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