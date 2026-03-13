from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    # Display 01 - get student data
    path('display/01/get_student_data/', views.Display01GetStudentDataView.as_view(), name='get_student_data'),
    # Display 01 - get recent checkins
    path('display/01/get_recent_checkins/', views.Display01GetRecentCheckinsView.as_view(), name='get_recent_checkins'),
    # Display 02 - get student data
    path('display/02/get_student_data/', views.Display02GetStudentDataView.as_view(), name='get_student_data'),
]