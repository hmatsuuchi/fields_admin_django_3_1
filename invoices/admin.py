from django.contrib import admin
# models
from invoices.models import PaymentMethod, Invoice, ServiceType, Tax, InvoiceItem

admin.site.register(PaymentMethod)
admin.site.register(Invoice)
admin.site.register(Tax)
admin.site.register(ServiceType)
admin.site.register(InvoiceItem)
