from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('events/all/', views.EventsAllView.as_view(), name='events_all'),
    path('events/details/', views.EventsDetailsView.as_view(), name='events_details'),

    # visit this path to import events from CSV
    # be sure to disable this path when not in use
    # path('events_import/', views.EventsImport, name='events_import'),
]