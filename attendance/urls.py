from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('attendance/single_date/', views.AttendanceForDateView.as_view(), name='attendance_for_date'),

    # visit this path to import attendance and attendance records from CSV
    # be sure to disable this path when not in use
    # 127.0.0.1:8000/api/attendance/attendance_import/
    # path('attendance_import/', views.AttendanceImport, name='attendance_import'),
]