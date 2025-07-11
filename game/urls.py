from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    # perform UUID lookup and get student data
    path('display/01/get_student_data/', views.GetStudentDataView.as_view(), name='get_student_data'),
    # get recent checkins
    path('display/01/get_recent_checkins/', views.GetRecentCheckinsView.as_view(), name='get_recent_checkins'),
]