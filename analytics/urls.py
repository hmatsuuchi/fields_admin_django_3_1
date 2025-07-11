from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('analytics/ml_predict_for_attendance_record/<int:attendance_record_id>/', views.StudentChurnModelPredictForAttendanceRecord.as_view(), name='ml_predict_for_attendance_record'),
]