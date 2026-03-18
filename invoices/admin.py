from django.contrib import admin
# models
from invoices.models import PaymentMethod, Invoice, ServiceType, Tax, InvoiceItem

# custom ordering for service types in the admin panel
@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    ordering = ['order']

admin.site.register(PaymentMethod)
admin.site.register(Invoice)
admin.site.register(Tax)
admin.site.register(InvoiceItem)
