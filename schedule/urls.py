from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('events/all/', views.EventsAllView.as_view(), name='events_all'),
]