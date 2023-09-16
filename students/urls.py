from django.urls import path
# VIEWS
from . import views

urlpatterns = [
     path('profiles/', views.ProfilesView.as_view(), name='student_profiles'),
     # visit this path to import student profiles from CSV
     # path('profiles_import/', views.ProfilesImport, name='profiles_import'),
]