from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('attendance/single_date/', views.AttendanceForDateView.as_view(), name='attendance_for_date'),
]