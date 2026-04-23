from django.urls import path
# VIEWS
from . import views

urlpatterns = [
        path('accounting/journal_entries/create/', views.JournalEntriesCreateView.as_view(), name='journal_entries_create'),
]