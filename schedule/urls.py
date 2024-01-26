from django.urls import path
# VIEWS
from . import views

urlpatterns = [
     path('events/', views.EventsForDateRangeListView.as_view(), name='events_list_view'),
]