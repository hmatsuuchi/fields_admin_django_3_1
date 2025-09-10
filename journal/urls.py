from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    # Fetch Journal Data
    path('journal/get_journal_for_profile/', views.GetJournalForProfileView.as_view(), name='get_journal_for_profile'),
    path('journal/get_journal_types/', views.GetJournalTypesView.as_view(), name='get_journal_types'),
    path('journal/get_active_instructors/', views.GetActiveInstructorsView.as_view(), name='get_active_instructors'),
    path('journal/get_profile_data/', views.GetProfileDataView.as_view(), name='get_profile_data'),

    # Create Journal Entry
    path('journal/create_journal_entry/', views.CreateJournalEntryView.as_view(), name='create_journal_entry'),

    # Archive Journal Entry
    path('journal/archive_journal_entry/', views.ArchiveJournalEntryView.as_view(), name='archive_journal_entry'),
]