from django.urls import path
# VIEWS
from . import views

urlpatterns = [

    path('journal/get_journal_for_profile/', views.GetJournalForProfileView.as_view(), name='get_journal_for_profile'),
    
    # visit this path to import journal from CSV
    # be sure to disable this path when not in use
    # 127.0.0.1:8000/api/journal/journal_import/
    # path('journal_import/', views.JournalImport, name='journal_import'),
]