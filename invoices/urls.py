from django.urls import path
# VIEWS
from . import views
# VIEWS
from .views import InvoiceListAllView, ProfilesListForSelectView

urlpatterns = [
    path('invoices/list/all/', InvoiceListAllView.as_view(), name='invoice-list-all'),
    path('invoices/profiles-list-for-select/', views.ProfilesListForSelectView.as_view(), name='profiles-list-for-select'),
]