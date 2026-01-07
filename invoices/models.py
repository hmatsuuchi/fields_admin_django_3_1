from django.db import models
# models
from students.models import Students

# ======== INVOICE MODELS =======

class PaymentMethod(models.Model):
    name                        = models.CharField(max_length=200, blank=False, null=False)
    order                       = models.IntegerField(blank=True, null=True)

    date_time_created           = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified          = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Payment Methods"

    def __str__(self):
        return f"{str(self.name)}"

class Invoice(models.Model):
    customer_name               = models.CharField(max_length=200, blank=True, null=True)
    customer_postal_code        = models.CharField(max_length=20, blank=True, null=True)
    customer_prefecture         = models.CharField(max_length=100, blank=True, null=True)
    customer_city               = models.CharField(max_length=100, blank=True, null=True)
    customer_address_line_1     = models.CharField(max_length=200, blank=True, null=True)
    customer_address_line_2     = models.CharField(max_length=200, blank=True, null=True)

    year                        = models.IntegerField(blank=False, null=False)
    month                       = models.IntegerField(blank=False, null=False)
    creation_date               = models.DateField(blank=False, null=False)
    transfer_date               = models.DateField(blank=True, null=True)
    issued_date                 = models.DateField(blank=True, null=True)
    paid_date                   = models.DateField(blank=True, null=True)

    issued                      = models.BooleanField(default=False, db_index=True)
    paid                        = models.BooleanField(default=False, db_index=True)

    student                     = models.ForeignKey(Students, on_delete=models.CASCADE, blank=False, null=False)
    payment_method              = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, blank=False, null=False)

    date_time_created           = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified          = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Invoices"

    def __str__(self):
        return f"{str(self.id)} - {str(self.student)} - {str(self.year)}/{str(self.month)}"
    
# ======== INVOICE ITEM MODELS =======
class Tax(models.Model):
    name                        = models.CharField(max_length=100, blank=False, null=False)
    rate                        = models.IntegerField(blank=False, null=False)

    default_value               = models.BooleanField(default=False, db_index=True)

    order                       = models.IntegerField(blank=True, null=True)

    date_time_created           = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified          = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Taxes"

    def __str__(self):
        return f"{str(self.name)} [{str(self.rate)}%]"
    
class ServiceType(models.Model):
    name                        = models.CharField(max_length=100, blank=False, null=False)
    price                       = models.IntegerField(blank=True, null=True)
    tax                         = models.ForeignKey(Tax, on_delete=models.CASCADE, blank=False, null=False)

    order                       = models.IntegerField(blank=True, null=True)

    date_time_created           = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified          = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Service Types"

    def __str__(self):
        return f"{str(self.name)} [{str(self.price)}]"
    
class InvoiceItem(models.Model):
    description                 = models.CharField(max_length=500, blank=False, null=False)
    quantity                    = models.IntegerField(blank=False, null=False)
    rate                        = models.IntegerField(blank=False, null=False)
    tax_rate                    = models.IntegerField(blank=False, null=False)

    invoice                     = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=False, null=False)
    service_type                = models.ForeignKey(ServiceType, on_delete=models.CASCADE, blank=False, null=False)
    tax_type                    = models.ForeignKey(Tax, on_delete=models.CASCADE, blank=False, null=False)
    
    date_time_created           = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified          = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Invoice Items"

    def __str__(self):
        return f"[{str(self.invoice)}] - {str(self.description)} - {str(self.rate)}"