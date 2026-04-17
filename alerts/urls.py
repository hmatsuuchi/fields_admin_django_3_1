from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('alerts/attendance_alerts/all/', views.AttendanceAlertsAllView.as_view(), name='attendance_alerts_all'),
    path('alerts/attendance_alerts/analyze/', views.AttendanceAlertsAnalyzeView.as_view(), name='attendance_alerts_analyze'),
]