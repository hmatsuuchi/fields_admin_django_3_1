from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('events/', views.EventsListView.as_view(), name='events'),
    path('events/details/', views.EventsDetailsView.as_view(), name='events_details'),
    path('events/remove_student_from_event/', views.RemoveStudentFromEvent.as_view(), name='remove_student_from_event'),
    path('events/add_student_to_event/', views.AddStudentToEvent.as_view(), name='add_student_to_event'),
    path('events/archive_event/', views.ArchiveEvent.as_view(), name='archive_event'),
    path('events/choices/', views.EventChoicesView.as_view(), name='event_choices'),

    # visit this path to import events from CSV
    # be sure to disable this path when not in use
    # path('events_import/', views.EventsImport, name='events_import'),
]