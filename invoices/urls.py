from django.urls import path
# VIEWS
from . import views
# VIEWS
from .views import InvoiceListAllView, InvoiceStatusAllView, InvoiceStatusBatchUpdateView, InvoiceCreateView, ProfilesListForSelectView, PaymentMethodsListForSelectView, ServiceTypesListForSelectView, TaxesListForSelectView

urlpatterns = [
    path('invoices/list/all/', InvoiceListAllView.as_view(), name='invoice-list-all'),

    path('invoices/status/all/', InvoiceStatusAllView.as_view(), name='invoice-status-all'),
    path('invoices/status/batch-update/', InvoiceStatusBatchUpdateView.as_view(), name='invoice-status-batch-update'),

    path('invoices/create/invoice/', InvoiceCreateView.as_view(), name='invoice-create'),

    path('invoices/profiles-list-for-select/', ProfilesListForSelectView.as_view(), name='profiles-list-for-select'),
    path('invoices/payment-methods-list-for-select/', PaymentMethodsListForSelectView.as_view(), name='payment-methods-list-for-select'),
    path('invoices/service-types-list-for-select/', ServiceTypesListForSelectView.as_view(), name='service-types-list-for-select'),
    path('invoices/taxes-list-for-select/', TaxesListForSelectView.as_view(), name='taxes-list-for-select'),
]