from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('dashboard/incomplete_attendance_for_instructor/', views.IncompleteAttendanceForInstructor.as_view(), name='incomplete_attendance_for_instructor'),
]