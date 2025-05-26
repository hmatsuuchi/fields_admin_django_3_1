import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Prefetch, Count
# authentication
from authentication.customAuthentication import CustomAuthentication
# group permission control
from authentication.permissions import isInStaffGroup
# models
from .models import Attendance, AttendanceRecord, AttendanceRecordStatus
from schedule.models import Events
from students.models import Students
# serializers
from .serializers import AttendanceSerializer, AttendanceDetailsSerializer, AttendanceRecordDetailsSerializer, UserInstructorSerializer, UserInstructorPreferenceSerializer, EventsChoiceListSerializer, StudentsChoiceListSerializer, AttendanceRecordForProfileDetailsSerializer
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
        
# attendance details
class AttendanceDetailsView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # POST - create attendance record
    def post(self, request, format=None):
        try:
            # get request data
            attendance_data = request.data

            # create new attendance record
            attendance_serializer = AttendanceDetailsSerializer(data=attendance_data)

            if attendance_serializer.is_valid():
                attendance_serializer.save()

                return Response(attendance_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(attendance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
    # PUT - update attendance record
    def put(self, request, format=None):
        try:
            # get request data
            data = request.data
            attendance_record_id = data.get('attendance_id')

            # get attendance record
            attendance_record = Attendance.objects.get(id=attendance_record_id)

            # update attendance record with new data
            attendance_serializer = AttendanceDetailsSerializer(attendance_record, data=data, partial=True)

            if attendance_serializer.is_valid():
                attendance_serializer.save()

                return Response(attendance_serializer.data, status=status.HTTP_200_OK)

            return Response(attendance_record_id, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Attendance.DoesNotExist:
            return Response({'error': 'Attendance record not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    # DELETE - delete attendance record
    def delete(self, request, format=None):
        try:
            # get request data
            data = request.data
            attendance_id = data.get('attendance_id')

            # get attendance
            attendance = Attendance.objects.get(id=attendance_id)

            # get attendance records
            attendance_records = attendance.attendance_records.all()

            # delete attendance records
            for record in attendance_records:
                record.delete()

            # delete attendance
            attendance.delete()

            return Response({
                'status': '200 OK',
                }, status=status.HTTP_200_OK)
        
        except AttendanceRecord.DoesNotExist:
            return Response({'error': 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)
        
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

# gets & updates user preferences for attendance app
class AttendanceUserPreferencesView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # GET - get user preferences
    def get(self, request, format=None):
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

        try:
            # get request data arguments
            user_preferences = request.data

            # check for instructor preference
            if 'pref_attendance_selected_instructor' in user_preferences and hasattr(request.user, 'userprofilesinstructors'):
                # get instructor id
                instructor_id = user_preferences.get('pref_attendance_selected_instructor')
                # set instructor preference if logged in user has instructor profile
                request.user.userprofilesinstructors.pref_attendance_selected_instructor = User.objects.get(id=instructor_id)
                request.user.userprofilesinstructors.save()

            # check for date preference
            if 'pref_attendance_selected_date' in user_preferences and hasattr(request.user, 'userprofilesinstructors'):
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
        
# attendance record details
class AttendanceRecordDetailsView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # POST - create attendance record
    def post(self, request, format=None):
        try:
            # get request data
            data = request.data

            # add current student grade to attendance record data
            data['grade'] = Students.objects.get(id=data['student']).grade.id

            # create new attendance record
            attendance_record_serializer = AttendanceRecordDetailsSerializer(data=data)

            if attendance_record_serializer.is_valid():
                created_attendance_record = attendance_record_serializer.save()

                # add attendance record to attendance
                attendance = Attendance.objects.get(id=data['attendance_id'])
                attendance.attendance_records.add(created_attendance_record)

                return Response(attendance_record_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(attendance_record_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
    # DELETE - delete attendance record
    def delete(self, request, format=None):
        try:
            # get request data
            data = request.data
            attendance_id = data.get('attendance_id')
            student_id = data.get('student_id')

            # get attendance record
            attendance = Attendance.objects.get(id=attendance_id)

            # delete attendance record
            attendance_record = attendance.attendance_records.filter(student=student_id)

            attendance_record.delete()

            return Response({
                'status': '200 OK',
                }, status=status.HTTP_200_OK)
        
        except AttendanceRecord.DoesNotExist:
            return Response({'error': 'Attendance record not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

# auto generate attendance records for date and instructor
class AutoGenerateAttendanceRecordsView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # POST - auto generate attendance records
    def post(self, request, format=None):
        try:
            # get request data
            data = request.data

            # get date and instructor id from data payload
            date = data.get('date')
            instructor_id = data.get('instructor_id')

            # get convert date string to day of week integer
            def get_day_of_week(date_string):
                date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d")
                day_of_week = date_object.weekday()

                return day_of_week
    
            # get instructor and day of week
            instructor = User.objects.get(id=instructor_id)
            day_of_week = get_day_of_week(date)

            # get all events from schedule for instructor and day of week
            schedule_events = Events.objects.filter(primary_instructor=instructor, day_of_week=day_of_week, archived=False).order_by("start_time").prefetch_related('students')

            # get all existing attendances for date and instructor
            existing_attendances = Attendance.objects.filter(date=date, instructor=instructor_id)
            existing_attendances_event_id_list = existing_attendances.values_list('linked_class', flat=True)

            # create new attendance records for events that do not have attendance records
            for event in schedule_events:
                if event.id not in existing_attendances_event_id_list:
                    attendance = Attendance()
                    attendance.linked_class = event
                    attendance.instructor = instructor
                    attendance.date = date
                    attendance.start_time = event.start_time
                    attendance.save()

                    for students in event.students.all():
                        attendance_record = AttendanceRecord()
                        attendance_record.student = students
                        attendance_record.status = AttendanceRecordStatus.objects.get(id=2)
                        attendance_record.grade = students.grade
                        attendance_record.save()

                        attendance.attendance_records.add(attendance_record)

            return Response({
                'status': '200 OK',
                }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

# get attendance for profile
class GetAttendanceForProfileView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # GET - get attendance for profile
    def get(self, request, format=None):
        try:
            # get request data
            profile_id = request.GET.get('profile_id')

            # get all attendance records for student
            attendance_records = AttendanceRecord.objects.filter(student=profile_id).order_by('-attendance_reverse_relationship__date', '-attendance_reverse_relationship__start_time').prefetch_related('attendance_reverse_relationship', 'attendance_reverse_relationship__linked_class', 'attendance_reverse_relationship__instructor', 'attendance_reverse_relationship__instructor__userprofilesinstructors', 'grade')

            # serialize attendance records
            attendance_records_serializer = AttendanceRecordForProfileDetailsSerializer(attendance_records, many=True)

            data = {
                'attendance_records': attendance_records_serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
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