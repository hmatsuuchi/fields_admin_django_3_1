from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('dashboard/incomplete_attendance_for_instructor/', views.IncompleteAttendanceForInstructorView.as_view(), name='incomplete_attendance_for_instructor'),
    path('dashboard/student_churn/', views.StudentChurnView.as_view(), name='student_churn'),
    path('dashboard/total_active_students/', views.TotalActiveStudentsView.as_view(), name='total_active_students'),
    path('dashboard/total_active_students_historical/', views.TotalActiveStudentsHistoricalView.as_view(), name='total_active_students_historical'),
    path('dashboard/at_risk_students/', views.AtRiskStudentsView.as_view(), name='at_risk_students'),
    path('dashboard/upcoming_birthdays/', views.UpcomingBirthdaysView.as_view(), name='upcoming_birthdays'),
    # OVERVIEW
    path('dashboard/incomplete_attendance_for_all_instructors/', views.IncompleteAttendanceForAllInstructorsView.as_view(), name='incomplete_attendance_for_all_instructors'),
]