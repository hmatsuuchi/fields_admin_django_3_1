from django.urls import path
# VIEWS
from . import views

urlpatterns = [
     path('profiles/', views.ProfilesListView.as_view(), name='student_profiles'),
     path('profiles/details/', views.ProfilesDetailsView.as_view(), name='student_profiles_details'),
     path('profiles/choices/', views.ProfilesChoicesView.as_view(), name='student_profiles_choices'),
     path('profiles/select_list/', views.ProfilesListForSelectView.as_view(), name='student_profiles_select'),
     
     # visit this path to import student profiles from CSV
     # be sure to disable this path when not in use
     # 127.0.0.1:8000/api/students/profiles_import/
     # path('profiles_import/', views.ProfilesImport, name='profiles_import'),
]