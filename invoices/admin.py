from django.contrib import admin
# models
from invoices.models import Invoice, InvoiceItem

admin.site.register(Invoice)
admin.site.register(InvoiceItem)
