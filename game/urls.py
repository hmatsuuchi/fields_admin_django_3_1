from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    # perform UUID lookup 
    path('display/01/', views.DisplayOne.as_view(), name='display_01'),
    # fetch all present attendance records for current day
    path('display/01/all_present_attendance_records_for_current_day/', views.AllPresentAttendanceRecordsForCurrentDay.as_view(), name='all_present_attendance_records_for_current_day'),

    # visit this path to import card UUID records from CSV
    # be sure to disable this path when not in use
    # http://127.0.0.1:8000/api/game/game/id_import/
    # path('game/id_import/', views.ImportCardUUID, name='card_uuid_import'),
]