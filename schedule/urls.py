from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('events/', views.EventsListView.as_view(), name='events'),
    path('events/details/', views.EventsDetailsView.as_view(), name='events_details'),
    path('events/remove_student_from_event/', views.RemoveStudentFromEventView.as_view(), name='remove_student_from_event'),
    path('events/add_student_to_event/', views.AddStudentToEventView.as_view(), name='add_student_to_event'),
    path('events/archive_event/', views.ArchiveEventView.as_view(), name='archive_event'),
    path('events/choices/', views.EventChoicesView.as_view(), name='event_choices'),

    # visit this path to import events from CSV
    # be sure to disable this path when not in use
    # 127.0.0.1:8000/api/schedule/events_import/
    # path('events_import/', views.EventsImport, name='events_import'),
]