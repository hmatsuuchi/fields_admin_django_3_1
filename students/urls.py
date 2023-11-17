from django.urls import path
# VIEWS
from . import views

urlpatterns = [
     path('profiles/', views.ProfilesView.as_view(), name='student_profiles'),
     path('profiles/details', views.ProfilesDetailsView.as_view(), name='student_profiles_details'),
     # visit this path to import student profiles from CSV
     # path('profiles_import/', views.ProfilesImport, name='profiles_import'),
]