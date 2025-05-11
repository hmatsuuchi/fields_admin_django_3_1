from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    # perform UUID lookup and get student data
    path('display/01/get_student_data/', views.GetStudentDataView.as_view(), name='get_student_data'),
    # get recent checkins
    path('display/01/get_recent_checkins/', views.GetRecentCheckinsView.as_view(), name='get_recent_checkins'),

    # visit this path to import card UUID records from CSV
    # be sure to disable this path when not in use
    # http://127.0.0.1:8000/api/game/game/id_import/
    # path('game/id_import/', views.ImportCardUUID, name='card_uuid_import'),
]