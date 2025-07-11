from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('attendance/single_date/', views.AttendanceForDateView.as_view(), name='attendance_for_date'),
    path('attendance/attendance_details/', views.AttendanceDetailsView.as_view(), name='attendance_details'),
    path('attendance/attendance_record_details/', views.AttendanceRecordDetailsView.as_view(), name='attendance_record_details'),
    path('attendance/update_attendance_record_status/', views.UpdateAttendanceRecordStatusView.as_view(), name='attendance_update_attendance_record_status'),
    path('attendance/instructor_choices/', views.InstructorChoicesView.as_view(), name='instructor_choices'),
    path('attendance/event_choices/', views.EventChoicesView.as_view(), name='event_choices'),
    path('attendance/student_choices/', views.StudentChoicesView.as_view(), name='student_choices'),
    path('attendance/user_preferences/', views.AttendanceUserPreferencesView.as_view(), name='attendance_user_preferences'),
    path('attendance/auto_generate_attendance_records/', views.AutoGenerateAttendanceRecordsView.as_view(), name='auto_generate_attendance_records'),
    path('attendance/get_attendance_for_profile/', views.GetAttendanceForProfileView.as_view(), name='get_attendance_for_profile'),
]