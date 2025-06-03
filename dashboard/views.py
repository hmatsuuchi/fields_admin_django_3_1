from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date, datetime, timedelta
from django.db.models import Count, Q, Min, Max
# authentication
from authentication.customAuthentication import CustomAuthentication
# group permission control
from authentication.permissions import isInStaffGroup
# models
from user_profiles.models import UserProfilesInstructors
from attendance.models import AttendanceRecord
from students.models import Students

# get all attendance records for single date
class IncompleteAttendanceForInstructor(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        try:
            # get the current user
            current_user = request.user

            # get all records for the instructor for the past month
            past_month = AttendanceRecord.objects.filter(attendance_reverse_relationship__instructor=current_user, attendance_reverse_relationship__date__gte=datetime.now() - timedelta(days=30), attendance_reverse_relationship__date__lte=datetime.now())

            # group the records by date
            past_month_by_date = past_month.order_by('-attendance_reverse_relationship__date').values('attendance_reverse_relationship__date')

            # annotate records with attendance status counts
            past_month_by_date_annotated = past_month_by_date.annotate(record_count_all=Count('id'), record_count_incomplete=Count('id', filter=Q(status=2)), record_count_present=Count('id', filter=Q(status=3)), record_count_absent=Count('id', filter=Q(status=4)))

            # get the instructor's working days preference
            instructor_profile = UserProfilesInstructors.objects.get(user=current_user)
            working_days = instructor_profile.pref_dashboard_working_days

            data = {
                'past_month_by_date_annotated': past_month_by_date_annotated,
                'pref_dashboard_working_days': working_days,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
# get student churn data
class StudentChurn(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):        
        try:
            # get students with four or more present attendance records
            students_with_attendance = (
                Students.objects
                .annotate(
                    present_count = Count('attendancerecord', filter=Q(attendancerecord__status=3)),
                    earliest_present = Min('attendancerecord__attendance_reverse_relationship__date', filter=Q(attendancerecord__status=3)),
                    latest_present = Max('attendancerecord__attendance_reverse_relationship__date', filter=Q(attendancerecord__status=3)),
                )
                .filter(present_count__gte=2)
                .order_by('earliest_present')
            )

            # for student in students_with_attendance:
            #     print(f"{student.last_name_romaji}, {student.first_name_romaji} - {student.present_count} [{student.earliest_present} ~ {student.latest_present}]")

            # create a list of years, months, starting students, ending students
            churn_data = []
            start_date = date(2022, 9, 1)
            today = date.today()
            current_date = start_date

            # iterate through each month from start_date to today
            while current_date <= today:
                # get the start of the month
                month_start = current_date.replace(day=1)
                # get the end of the month
                next_month = (month_start + timedelta(days=31)).replace(day=1)
                month_end = next_month - timedelta(days=1)

                # Students who started in this month
                starting_students = [
                    student for student in students_with_attendance
                    if month_start <= student.earliest_present <= month_end
                ]

                # Students who ended in this month and latest_present is more than 4 weeks ago
                ending_students = [
                    student for student in students_with_attendance
                    if month_start <= student.latest_present <= month_end and (today - student.latest_present).days > 28
                ]

                churn_data.insert(0, {
                    'year': month_start.year,
                    'month': month_start.month,
                    'starting_students_count': len(starting_students),
                    'ending_students_count': len(ending_students),
                    'starting_students_list': [
                        {
                            'id': student.id,
                            'last_name_romaji': student.last_name_romaji,
                            'first_name_romaji': student.first_name_romaji,
                            'start_date': student.earliest_present,
                        }
                        for student in starting_students
                    ],
                    'ending_students_list': [
                        {
                            'id': student.id,
                            'last_name_romaji': student.last_name_romaji,
                            'first_name_romaji': student.first_name_romaji,
                            'end_date': student.latest_present,
                        }
                        for student in ending_students
                    ],
                })

                # move to the next month
                current_date = next_month

            return Response(churn_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)