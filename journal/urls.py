from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    path('journal/get_journal_for_profile/', views.GetJournalForProfileView.as_view(), name='get_journal_for_profile'),
]