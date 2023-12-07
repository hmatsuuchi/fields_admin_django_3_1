from django.urls import path
# VIEWS
from . import views

urlpatterns = [
     path('profiles/', views.ProfilesView.as_view(), name='student_profiles'),
     path('profiles/details', views.ProfilesDetailsView.as_view(), name='student_profiles_details'),
     path('profiles/create', views.ProfilesCreateView.as_view(), name='student_profiles_create'),
     path('profiles/choices', views.ProfilesChoicesView.as_view(), name='student_profiles_choices'),
     
     # visit this path to import student profiles from CSV
     # path('profiles_import/', views.ProfilesImport, name='profiles_import'),
]