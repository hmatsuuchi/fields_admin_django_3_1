from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# group permission control
from authentication.permissions import isInStaffGroup
# authentication
from authentication.customAuthentication import CustomAuthentication
# models
from .models import Events, EventType
from django.contrib.auth.models import User
# serializers
from .serializers import EventsSerializer, InstructorSerializer
# importing csv
import csv
from students.models import Students
from django.http import JsonResponse

# get all events for single date
class EventsAllView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        try:
            # get all events for date
            events = Events.objects.all().filter(archived=False).prefetch_related('students', 'event_type', 'primary_instructor')
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
        
# used to import events from CSV     
def EventsImport(request):
    print('')
    print('======= IMPORTING EVENTS =======')
    print('')

    events_all = Events.objects.all()
    events_all.delete()

    with open("./static/class_list_classlist.csv") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            print(row)

            event = Events()
            event.id = row[0]
            event.event_name = row[1]
            event.event_type = EventType.objects.get(id=row[6])
            if row[7] == '2':
                event.primary_instructor = User.objects.get(id=4)
            elif row[7] == '4':
                event.primary_instructor = User.objects.get(id=5)
            elif row[7] == '3':
                event.primary_instructor = User.objects.get(id=6)
            event.day_of_week = int(row[3]) - 1
            if row[4] != "NULL":
                event.start_time = row[4]
            event.archived = row[5]

            event.save()

    print('')
    print('======= IMPORT EVENTS COMPLETE =======')
    print('')

    with open("./static/class_list_classlist_students.csv") as file:
        print('')
        print('======= IMPORTING CLASS LISTS =======')
        print('')

        reader = csv.reader(file)
        next(reader)

        for row in reader:
            print(row)

            event = Events.objects.get(id=row[1])
            event.students.add(Students.objects.get(id=row[2]))

        print('')
        print('======= IMPORT CLASS LISTS COMPLETE =======')
        print('')

    data = {
        'status': '200 OK',
    }

    return JsonResponse(data)