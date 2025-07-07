from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('analytics/ml_train/', views.StudentChurnModelTrain.as_view(), name='ml_train'),
    path('analytics/ml_predict_for_single_student/<int:student_id>/', views.StudentChurnModelPredictForSingleStudent.as_view(), name='ml_predict_for_single_student'),
    path('analytics/ml_predict_for_attendance_record/<int:attendance_record_id>/', views.StudentChurnModelPredictForAttendanceRecord.as_view(), name='ml_predict_for_attendance_record'),
    path('analytics/ml_predict_for_active_students/', views.StudentChurnModelPredictForActiveStudents.as_view(), name='ml_predict_for_active_students'),
]