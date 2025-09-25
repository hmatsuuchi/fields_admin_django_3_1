from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date, datetime, timedelta
from django.db.models import Count, Q, Min, Max, Prefetch
# authentication
from authentication.customAuthentication import CustomAuthentication
# group permission control
from authentication.permissions import isInStaffGroup
# models
from user_profiles.models import UserProfilesInstructors
from attendance.models import AttendanceRecord
from students.models import Students
from analytics.models import HighestActiveStudentCount, AtRiskStudents
from schedule.models import Events
# serializers
from dashboard.serializers import AtRiskStudentSerializer
from dashboard.serializers import UpcomingBirthdayStudentSerializer

# get all attendance records for single date
class IncompleteAttendanceForInstructorView(APIView):
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
class StudentChurnView(APIView):
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

            # create a list of years, months, starting students, ending students
            churn_data = []
            today = date.today()
            start_date = today - timedelta(days=365 * 2)  # 2 years ago
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

                churn_data.append({
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
        
# get total active students data
class TotalActiveStudentsView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):        
        try:
            cutoff_date = date.today() - timedelta(days=28)

            # active students are those with at least two present (status=3) attendance records, and at least one of those records is within the last 28 days
            active_students = (
                Students.objects
                .annotate(
                    attendance_count=Count('attendancerecord', filter=Q(attendancerecord__status=3)),
                    most_recent=Max('attendancerecord__attendance_reverse_relationship__date', filter=Q(attendancerecord__status=3))
                )
                .filter(
                    attendance_count__gte=2,
                    most_recent__gte=cutoff_date
                )
                .distinct()
            )

            # gets the highest active student count
            highest_active_student_count = HighestActiveStudentCount.objects.order_by('-active_student_count').first()

            if not highest_active_student_count:
                # if no records exist, create a new record with the current count
                highest_active_student_count = HighestActiveStudentCount.objects.create(
                    active_student_count=active_students.count()
                )
            elif highest_active_student_count.active_student_count < active_students.count():
                # if the current count is higher than the stored count, create a new record with the current count
                highest_active_student_count = HighestActiveStudentCount.objects.create(
                    active_student_count=active_students.count()
                )


            data = {
                'total_active_students_count': active_students.count(),
                'highest_active_student_count': {
                    'count': highest_active_student_count.active_student_count,
                    'date': highest_active_student_count.date_time_created,
                },
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# get list of students at risk of churn
class AtRiskStudentsView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):        
        try:

            # get at risk student list
            at_risk_students = AtRiskStudents.objects.all().order_by('-date_time_created')

            # serialize student list
            serializer = AtRiskStudentSerializer(at_risk_students, many=True)

            data = {
                'at_risk_students': serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# get list of students with upcoming birthdays
class UpcomingBirthdaysView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):        
        try:
            start_date          = datetime.now() # today
            day_of_week_today   = start_date.weekday() # day of the week (0=Monday, 6=Sunday)

            # date_offset         = 0
            # start_date          = datetime.now() + timedelta(days=date_offset)
            # day_of_week_today   = start_date.weekday()

            # create a list of (month, day) tuples for the next 7 days
            date_list = [
                (d.month, d.day)
                for d in (start_date + timedelta(days=i) for i in range(7))
            ]

            # create a Q object to hold the OR conditions
            q_objects = Q()
            for month, day in date_list:
                q_objects |= Q(birthday__month=month, birthday__day=day)

            # get all active students
            active_students = Students.objects.filter(status=2)

            # filter by active lessons on current day of the week
            students_with_lessons_today = active_students.filter(events__day_of_week=day_of_week_today, events__archived=False).distinct()

            # students with birthday data
            students_with_birthday_data = students_with_lessons_today.filter(
                birthday__isnull=False
            )
            
            # students with birthdays within the next 7 days
            students_with_upcoming_birthdays = students_with_birthday_data.filter(q_objects).order_by('events__start_time')

            # get related objects to reduce queries
            students_with_upcoming_birthdays = students_with_upcoming_birthdays.prefetch_related(Prefetch('events_set', queryset=Events.objects.filter(day_of_week=day_of_week_today, archived=False))
)

            # serialize data
            serializer = UpcomingBirthdayStudentSerializer(students_with_upcoming_birthdays, many=True)

            birthday_data = serializer.data

            return Response(birthday_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)