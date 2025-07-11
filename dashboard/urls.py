from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('dashboard/incomplete_attendance_for_instructor/', views.IncompleteAttendanceForInstructorView.as_view(), name='incomplete_attendance_for_instructor'),
    path('dashboard/student_churn/', views.StudentChurnView.as_view(), name='student_churn'),
    path('dashboard/total_active_students/', views.TotalActiveStudentsView.as_view(), name='total_active_students'),
    path('dashboard/at_risk_students/', views.AtRiskStudentsView.as_view(), name='at_risk_students'),
]