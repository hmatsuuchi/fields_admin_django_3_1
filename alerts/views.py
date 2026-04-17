from django.shortcuts import render
import datetime, statistics
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth.models import User
# rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# authentication
from authentication.customAuthentication import CustomAuthentication
from authentication.permissions import isInSuperusersGroup
# models
from alerts.models import AttendanceAlert
from attendance.models import Attendance, AttendanceRecord
from user_profiles.models import UserProfilesInstructors
# serializers
from .serializers import AttendanceAlertSerializer



# get all incomplete recent attendance records for an instructor
class AttendanceAlertsAllView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInSuperusersGroup])

    def get(self, request, format=None):
        try:
            # get all attendance alerts
            attendance_alerts = AttendanceAlert.objects.all().order_by('-warning_date')

            # serialize data
            serializer = AttendanceAlertSerializer(attendance_alerts, many=True)

            data = {
                'attendance_alerts': serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# analyze attendance
class AttendanceAlertsAnalyzeView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInSuperusersGroup])

    def get(self, request, format=None):
        try:
            analysis_date_range = 12 # number of weeks to analyze
            display_date_range = 4 # number of weeks to display in response (must be less than or equal to analysis_date_range)

            # if today is not Monday, find the most recent Monday
            most_recent_monday = timezone.localdate()
            while most_recent_monday.weekday() != 0: # Monday=0, Tuesday=1, ..., Sunday=6
                most_recent_monday -= datetime.timedelta(days=1)

            # set the date range for analysis always starting on Monday and ending on Sunday
            range_start_date = most_recent_monday - datetime.timedelta(weeks=analysis_date_range)
            range_end_date = most_recent_monday - datetime.timedelta(days=1)

            # get all attendance records from the specified date range            
            base_attendance_records = AttendanceRecord.objects.filter(
                attendance_reverse_relationship__date__gte=range_start_date,
                attendance_reverse_relationship__date__lte=range_end_date,
            )
            
            # group attendance records by instructor and date, and count total and incomplete records for each group
            grouped_attendance_records = base_attendance_records.values(
                'attendance_reverse_relationship__instructor',
                'attendance_reverse_relationship__date',
                'attendance_reverse_relationship__date__week_day', # Sunday=1, Monday=2, ..., Saturday=7
            ).order_by(
                'attendance_reverse_relationship__instructor',
                'attendance_reverse_relationship__date',
            ).annotate(
                total_records=Count('id'),
                incomplete_records=Count('id', filter=Q(status=2)),
            )

            # creates a lookup dictionary for analytics data, where the key is a tuple of (instructor_id, date) and the value is the corresponding analytics data for that instructor and date (total_records and incomplete_records), used to efficiently populate analytics data for each instructor and day of week in the date range
            analytics_data_lookup_dictionary = {
                (
                    row['attendance_reverse_relationship__instructor'],
                    row['attendance_reverse_relationship__date'],
                ): row for row in grouped_attendance_records
            }

            # derives instrucor list from attendance records queryset
            instructor_list = base_attendance_records.values(
                'attendance_reverse_relationship__instructor__id',
                'attendance_reverse_relationship__instructor__userprofilesinstructors__last_name_romaji',
                'attendance_reverse_relationship__instructor__userprofilesinstructors__first_name_romaji',
                ).distinct()
                        
            # initializes analytics data list for response
            analytics_data = []

            # iterates through instructor list            
            for instructor in instructor_list:
                day_of_week_data = [] # contains analytics data for each day of week (Monday, Tuesday, ..., Sunday)

                # iterates through each day of week (Monday, Tuesday, ..., Sunday)
                for day_of_week in range(0, 7):
                    date = range_start_date + datetime.timedelta(days=day_of_week) # first day of week in date range

                    attendance_records_for_day_of_week = [] # attendance records for the current instructor and day of week (Monday, Tuesday, ..., Sunday) in date range
                    attendance_records_counts = [] # list of total attendance record counts for each day of week in date range, used to calculate mean and standard deviation for anomaly detection

                    # iterates through each week in date range for the current day of week (Monday, Tuesday, ..., Sunday)
                    while date <= range_end_date:
                        # finds analytics data for the current instructor and date
                        matching_instructor_and_date = analytics_data_lookup_dictionary.get(
                            (
                                instructor['attendance_reverse_relationship__instructor__id'],
                                date,
                            )
                        )

                        # if analytics data exists for the current instructor and date, use it to populate attendance_records_for_day_of_week and attendance_records_counts, otherwise populate with 0 records
                        if matching_instructor_and_date:
                            total_records = matching_instructor_and_date['total_records']
                            incomplete_records = matching_instructor_and_date['incomplete_records']

                            attendance_records_counts.append(total_records)

                            attendance_records_for_day_of_week.append({
                                'date': date,
                                'total_records': total_records,
                                'incomplete_records': incomplete_records,
                            })

                        # if no analytics data exists for the current instructor and date, populate with 0 records
                        else:
                            attendance_records_counts.append(0)

                            attendance_records_for_day_of_week.append({
                                'date': date,
                                'total_records': 0,
                                'incomplete_records': 0,
                            })

                        date += datetime.timedelta(weeks=1)

                    # calculate mean and standard deviation for the current instructor and day of week (Monday, Tuesday, ..., Sunday) using attendance_records_counts, and flag any records in attendance_records_for_day_of_week that are anomalies (i.e. total_records is more than 1 standard deviation away from the mean)
                    mean = statistics.mean(attendance_records_counts)
                    std_dev = statistics.stdev(attendance_records_counts)

                    # flagging attendance records that are anomalies based on mean and standard deviation
                    flagged_attendance_records_for_day_of_week = []
                    for record in attendance_records_for_day_of_week:
                        if record['total_records'] < mean - std_dev or record['total_records'] > mean + std_dev:
                            record['flagged'] = True
                        else:
                            record['flagged'] = False

                        flagged_attendance_records_for_day_of_week.append(record)
                        


                    day_of_week_data.append({
                        'day_of_week': day_of_week, # Monday=0, Tuesday=1, ..., Sunday=6
                        'attendance_records_for_day_of_week': flagged_attendance_records_for_day_of_week[::-1][:display_date_range], # reverse order to have most recent dates first, and limit to display_date_range
                        'attendance_records_mean': mean,
                        'attendance_records_std_dev': std_dev,
                    })

                analytics_data.append({
                    'instructor_id': instructor['attendance_reverse_relationship__instructor__id'],
                    'instructor_last_name_romaji': instructor['attendance_reverse_relationship__instructor__userprofilesinstructors__last_name_romaji'],
                    'instructor_first_name_romaji': instructor['attendance_reverse_relationship__instructor__userprofilesinstructors__first_name_romaji'],
                    'day_of_week_data': day_of_week_data,
                })


            response_data = {
                'analytics': analytics_data,
                }

            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)