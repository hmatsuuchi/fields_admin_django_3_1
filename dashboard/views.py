from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.db.models import Count, Q
# authentication
from authentication.customAuthentication import CustomAuthentication
# group permission control
from authentication.permissions import isInStaffGroup
# models
from user_profiles.models import UserProfilesInstructors
from attendance.models import AttendanceRecord

# get all attendance records for single date
class IncompleteAttendanceForInstructor(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        try:
            # get the current user
            current_user = request.user

            # get all records for the instructor for the past month
            past_month = AttendanceRecord.objects.filter(attendance__instructor=current_user, attendance__date__gte=datetime.now() - timedelta(days=30), attendance__date__lte=datetime.now())

            # group the records by date
            past_month_by_date = past_month.order_by('-attendance__date').values('attendance__date')

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