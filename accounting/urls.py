from django.urls import path
# VIEWS
from . import views

urlpatterns = [
        path('accounting/journal_entries/create/', views.JournalEntriesCreateView.as_view(), name='journal_entries_create'),
        path('accounting/accounts/list/', views.AccountListForDropdownMenuView.as_view(), name='account_list_dropdown'),
        path('accounting/accounts/summary/', views.BalanceSheetView.as_view(), name='account_summary'),
        path('accounting/account/transactions/', views.AccountActivityView.as_view(), name='account_activity'),
]