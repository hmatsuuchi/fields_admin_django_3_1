from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('events/single_date/', views.EventsForSingleDateListView.as_view(), name='events_single_date_view'),
     path('events/', views.EventsForDateRangeListView.as_view(), name='events_list_view'),
]