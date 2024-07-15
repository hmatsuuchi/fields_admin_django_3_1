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
from .serializers import EventsSerializer, EventCreateSerialzizer, InstructorSerializer
# importing csv
import csv
from students.models import Students
from django.http import JsonResponse

# get all events for single date
class EventsListView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        try:
            # get all events for date
            events = Events.objects.all().filter(archived=False).select_related('event_type', 'primary_instructor').prefetch_related('students')
            # serialize events
            event_serializer = EventsSerializer(events, many=True)

            # get all instructors for events
            # instructors = User.objects.filter(events__in=events).distinct().order_by('username')
            instructors = User.objects.filter(userprofilesinstructors__archived=False).order_by('username')
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

# event details
class EventsDetailsView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # GET - event details
    def get(self, request, format=None):
        try:
            event_id = request.GET.get('event_id')
            event = Events.objects.get(id=event_id)
            serializer = EventsSerializer(event)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        json_data = request.data.copy()

        try:
            serializer = EventCreateSerialzizer(data=json_data)

            if serializer.is_valid():
                serializer.save()
                data = {
                    "eventId": serializer.data['id'],
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

# event type choice list
class EventChoicesView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # GET - event type choice list
    def get(self, request, format=None):
        try:
            event_type_choices = EventType.objects.all().order_by('order')
            primary_instructor_choices = User.objects.filter(groups__name='Instructors').order_by('username')

            data = {
                'event_type_choices': event_type_choices.values('id', 'name'),
                'primary_instructor_choices': primary_instructor_choices.values('id', 'username', 'userprofilesinstructors__last_name_romaji', 'userprofilesinstructors__first_name_romaji', 'userprofilesinstructors__last_name_katakana', 'userprofilesinstructors__first_name_katakana', 'userprofilesinstructors__last_name_kanji', 'userprofilesinstructors__first_name_kanji'),
            }


            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

# remove student from event        
class RemoveStudentFromEvent(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # PUT - remove student from event
    def put(self, request):
        try:
            # get event_id from request
            event_id = request.data['event_id']
            # get event
            event = Events.objects.get(id=event_id)
            
            # get student_id from request
            student_id = request.data['student_id']
            # get student
            student = Students.objects.get(id=student_id)

            # removes student from event
            event.students.remove(student)

            data = {
                'status': '200 OK',
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
# add student to event       
class AddStudentToEvent(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # PUT - add student to event
    def put(self, request):
        try:
            # get event_id from request
            event_id = request.data['event_id']
            # get event
            event = Events.objects.get(id=event_id)
            
            # get student_id from request
            student_id = request.data['student_id']
            # get student
            student = Students.objects.get(id=student_id)

            # removes student from event
            event.students.add(student)

            data = {
                'status': '200 OK',
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
# archive event       
class ArchiveEvent(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # PUT - add student to event
    def put(self, request):
        try:
            # get event_id from request
            event_id = request.data['event_id']
            # get event
            event = Events.objects.get(id=event_id)
            # archive event
            event.archived = True
            # save event
            event.save()

            data = {
                'status': '200 OK',
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