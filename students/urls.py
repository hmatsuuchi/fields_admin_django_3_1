from django.urls import path
# VIEWS
from . import views

urlpatterns = [
     path('profiles/', views.ProfilesListView.as_view(), name='student_profiles'),
     path('profiles/details/', views.ProfilesDetailsView.as_view(), name='student_profiles_details'),
     path('profiles/choices/', views.ProfilesChoicesView.as_view(), name='student_profiles_choices'),
     path('profiles/select_list/', views.ProfilesListForSelectView.as_view(), name='student_profiles_select'),
]