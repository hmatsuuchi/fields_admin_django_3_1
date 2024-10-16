from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
# authentication
from authentication.customAuthentication import CustomAuthentication
# group permission control
from authentication.permissions import isInStaffGroup
# models
from .models import Attendance, AttendanceRecord, AttendanceRecordStatus
from schedule.models import Events
from students.models import Students
# serializers
from .serializers import AttendanceSerializer, UserInstructorSerializer, UserInstructorPreferenceSerializer, EventsChoiceListSerializer, StudentsChoiceListSerializer
# importing csv
import csv
from django.http import JsonResponse

# get all attendance records for single date
class AttendanceForDateView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        try:
            # get date parameter from request
            date = request.GET.get('date')
            instructor_id = request.GET.get('instructor_id')

            # get all attendance records for date
            attendance = Attendance.objects.filter(date=date, instructor=instructor_id).order_by('start_time').prefetch_related('attendance_records')

            # serialize attendance
            attendance_serialzer = AttendanceSerializer(attendance, many=True)

            data = {
                'attendance': attendance_serialzer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

# update attendance record status
class UpdateAttendanceRecordStatusView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # PUT - update attendance record status
    def put(self, request, format=None):
        try:
            # get request data
            attendance_record_id = request.data['attendance_record_id']
            attendance_record_status_id = request.data['attendance_record_status_id']

            # get attendance record
            attendance_record = AttendanceRecord.objects.get(id=attendance_record_id)

            # update attendance record status
            attendance_record.status = AttendanceRecordStatus.objects.get(id=attendance_record_status_id)
            attendance_record.save()

            return Response({
                'status': '200 OK',
                'attendance_record_id': attendance_record.id,
                'attendance_reecord_status': attendance_record.status.id
                }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
# primary instructor choice list
class InstructorChoicesView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # GET - instructor choice list
    def get(self, request, format=None):
        try:
            # get all primary instructors
            primary_instructor_choices = User.objects.filter(groups__name='Instructors').order_by('username')

            # serialize primary instructors
            primary_instructor_choices_serializer = UserInstructorSerializer(primary_instructor_choices, many=True)

            data = {
                'primary_instructor_choices': primary_instructor_choices_serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
# event choice list
class EventChoicesView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # GET - events choice list
    def get(self, request, format=None):
        try:
            # get all events
            event_choices = Events.objects.all().filter(archived=False).prefetch_related('primary_instructor', 'event_type', 'students')

            # serialize events
            event_choices_serializer = EventsChoiceListSerializer(event_choices, many=True)

            data = {
                'event_choices': event_choices_serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

# student choice list
class StudentChoicesView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # GET - student choice list
    def get(self, request, format=None):
        try:
            # get all students
            student_choices = Students.objects.all().filter(archived=False)

            # serialize students
            student_choices_serializer = StudentsChoiceListSerializer(student_choices, many=True)

            data = {
                'student_choices': student_choices_serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

# gets user preferences for attendance app
class AttendanceUserPreferencesView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # GET - get user preferences
    def get(self, request, format=None):
        print('====================================')
        print('AttendanceUserPreferencesView - GET')
        print('====================================')
        try:
            # get user preferences
            user_preferences = request.user.userprofilesinstructors

            # serialize user preferences
            user_preferences_serializer = UserInstructorPreferenceSerializer(user_preferences)

            data = {
                'user_preferences': user_preferences_serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
    # PUT - update user preferences
    def put(self, request, format=None):
        print('====================================')
        print('AttendanceUserPreferencesView - PUT')
        print('====================================')

        try:
            # get request data arguments
            user_preferences = request.data

            print(user_preferences)

            # check for instructor preference
            if 'pref_attendance_selected_instructor' in user_preferences and hasattr(request.user, 'userprofilesinstructors'):
                print("updating instructor preference")
                # get instructor id
                instructor_id = user_preferences.get('pref_attendance_selected_instructor')
                # set instructor preference if logged in user has instructor profile
                request.user.userprofilesinstructors.pref_attendance_selected_instructor = User.objects.get(id=instructor_id)
                request.user.userprofilesinstructors.save()

            # check for date preference
            if 'pref_attendance_selected_date' in user_preferences and hasattr(request.user, 'userprofilesinstructors'):
                print("updating date preference")
                # get date
                date = user_preferences.get('pref_attendance_selected_date')
                # set date preference if logged in user has instructor profile
                request.user.userprofilesinstructors.pref_attendance_selected_date = date
                request.user.userprofilesinstructors.save()

            return Response({
                'status': '200 OK',
                }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
# used to import attendance records from CSV
def AttendanceImport(request):
    print('')
    print('======= IMPORTING ATTENDANCE & ATTENDANCE RECORDS =======')
    print('')

    # delete all attendance
    Attendance.objects.all().delete()
    # delete all attendance records
    AttendanceRecord.objects.all().delete()

    # import attendance CSV
    with open('./static/attendance_attendance.csv') as file:
        attendance_reader = csv.reader(file)
        next(attendance_reader)

        for row in attendance_reader:
            if row[1] != 'NULL':
                print(row)

                attendance = Attendance()
                attendance.id = row[0]
                attendance.linked_class = Events.objects.get(id=row[1])
                attendance.date = row[2]
                attendance.start_time = row[3]

                # translates csv values to instructor IDs
                def instructor_id(csv_id):
                    if csv_id == 2:
                        return 4
                    if csv_id == 3:
                        return 6
                    if csv_id == 4:
                        return 5
                    
                attendance.instructor = User.objects.get(id=instructor_id(int(row[4])))

                attendance.save()

    # import attendance records CSV
    with open('./static/attendance_studentattendance.csv') as file:
        attendance_record_reader = csv.reader(file)
        next(attendance_record_reader)

        for row in attendance_record_reader:
            print(row)

            attendance_record = AttendanceRecord()
            attendance_record.id = row[0]
            
            # translates csv values to attendance status IDs
            def record_status(csv_status):
                if csv_status == 0:
                    return 2
                if csv_status == 1:
                    return 3
                if csv_status == 2:
                    return 4
                
            attendance_record.status = AttendanceRecordStatus.objects.get(id=record_status(int(row[1])))
            attendance_record.student = Students.objects.get(id=row[2])

            attendance_record.save()

            attendance = Attendance.objects.get(id=row[3])
            attendance.attendance_records.add(attendance_record)
            attendance.save()

    return JsonResponse({'status': '200 OK'})