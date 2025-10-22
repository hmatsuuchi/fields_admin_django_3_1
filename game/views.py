from django.db.models import OuterRef, Subquery, Count, Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# authentication
from authentication.customAuthentication import CustomAuthentication
# group permission control
from authentication.permissions import isInDisplaysGroup
# models
from .models import CardUUID, CheckIn
from students.models import Students
from attendance.models import AttendanceRecord
# serializers
from .serializers import AttendanceRecordSerializer, CheckInSerializer
# importing csv
import csv

# get student data based on card UUID
class GetStudentDataView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInDisplaysGroup])

    def get(self, request, format=None):
        try:
            # get UUID from request
            card_uuid = request.GET.get('card_uuid')

            # get student record, attendance data and attendance count
            card_record = get_object_or_404(
                CardUUID.objects.select_related('linked_student').annotate(
                    attendance_present_count=Count(
                        'linked_student__attendancerecord',
                        filter=Q(linked_student__attendancerecord__status=3)
                    )
                ),
                card_uuid=card_uuid
            )

            # get linked student
            student = card_record.linked_student
            # count attendance records for present status
            attendance_present_count = card_record.attendance_present_count

            # === no need to fetch and serialize attendance records yet as they are not displayed in frontend ===
            # get related attendance records
            # attendance_records = AttendanceRecord.objects.filter(student=student).order_by('attendance_reverse_relationship__date').select_related('status').prefetch_related('attendance_reverse_relationship')

            # serialize attendance records
            # attendance_records_serialzer = AttendanceRecordSerializer(attendance_records, many=True)

            # create checkin record
            CheckIn.objects.create(
                student=student,
                attendance_present_count=attendance_present_count,
            )

            data = {
                'card_uuid': card_uuid,
                'student_last_name_romaji': student.last_name_romaji,
                'student_first_name_romaji': student.first_name_romaji,
                'student_grade_verbose': student.grade_verbose,
                'attendance_present_count': attendance_present_count,
                # 'attendance_records': attendance_records_serialzer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

# get recent checkins
class GetRecentCheckinsView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInDisplaysGroup])

    def get(self, request, format=None):
        try:
            # Subquery to get the most recent check-in for each student
            latest_checkins = CheckIn.objects.filter(
                student=OuterRef('student'),
            ).order_by('-date_time_created')

            # Filter the queryset to include only the most recent check-ins
            checkins = CheckIn.objects.filter(
                id=Subquery(latest_checkins.values('id')[:1])
            ).order_by('-date_time_created'
            ).select_related('student')[:15]

            # Serialize the queryset
            checkins_serializer = CheckInSerializer(checkins, many=True)

            return Response(checkins_serializer.data, status=status.HTTP_200_OK)
        
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