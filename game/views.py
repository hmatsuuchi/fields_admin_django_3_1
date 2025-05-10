from datetime import date
from django.db.models import Count, Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# authentication
from authentication.customAuthentication import CustomAuthentication
# group permission control
from authentication.permissions import isInDisplaysGroup
# models
from .models import CardUUID
from students.models import Students
from attendance.models import AttendanceRecord
# serializers
from .serializers import AttendanceRecordSerializer, AllPresentAttendanceRecordsForCurrentDaySerializer
# importing csv
import csv

class DisplayOne(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInDisplaysGroup])

    def get(self, request, format=None):
        try:
            # get UUID from request
            card_uuid = request.GET.get('card_uuid')
            # lookup card UUID
            card_record = CardUUID.objects.get(card_uuid=card_uuid)

            # get linked student
            student = Students.objects.get(id=card_record.linked_student.id)

            # get related attendance records
            attendance_records = AttendanceRecord.objects.filter(student=student).order_by('attendance_reverse_relationship__date').prefetch_related('attendance_reverse_relationship')
            # filter attendance records for present status
            attendance_present_records = attendance_records.filter(student=student, status=3)
            # count attendance records for present status
            attendance_present_count = attendance_present_records.count()

            # serialize attendance records
            attendance_records_serialzer = AttendanceRecordSerializer(attendance_records, many=True)

            data = {
                'card_uuid': card_uuid,
                'student_last_name_romaji': student.last_name_romaji,
                'student_first_name_romaji': student.first_name_romaji,
                'student_grade_verbose': student.grade_verbose,
                'attendance_present_count': attendance_present_count,
                'attendance_records': attendance_records_serialzer.data,

            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


# all present attendance records for current day
class AllPresentAttendanceRecordsForCurrentDay(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInDisplaysGroup])

    def get(self, request, format=None):
        try:
            # get current date
            date_today = date.today()
            
            # get all attendance records for current date
            attendance_records = AttendanceRecord.objects.filter(status=3, attendance_reverse_relationship__date=date_today).annotate(present_attendance_records_count = Count('student__attendancerecord', filter=Q(student__attendancerecord__status=3)))

            # serialize attendance records
            attendance_records_serialzer = AllPresentAttendanceRecordsForCurrentDaySerializer(attendance_records, many=True)

            return Response(attendance_records_serialzer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
# used to import attendance records from CSV
def ImportCardUUID(request):
    print('')
    print('======= IMPORTING CARD UUIDs =======')
    print('')

    # delete all previous records
    CardUUID.objects.all().delete()

    # import card UUID CSV
    with open('./static/game_cardindex.csv') as file:
        card_index_reader = csv.reader(file)
        next(card_index_reader)

        for row in card_index_reader:
            CardUUID.objects.create(
                card_uuid=row[1],
                linked_student=Students.objects.get(id=row[2]),
            )

    print('======= IMPORT COMPLETE =======')

    return JsonResponse({'status': '200 OK'})