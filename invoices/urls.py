from django.urls import path
# VIEWS
from . import views
# VIEWS
from .views import InvoiceListAllView

urlpatterns = [
    path('invoices/list/all/', InvoiceListAllView.as_view(), name='invoice-list-all'),
]