from rest_framework import serializers
# MODELS
from .models import Invoice, PaymentMethod, InvoiceItem, ServiceType, Tax
from students.models import Students


# ========== INVOICE LIST ALL SERIALIZER ==========

# Payment Method Serializer
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

# Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'

# Tax Serializer
class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'

# Service Type Serializer
class ServiceTypeSerializer(serializers.ModelSerializer):
    tax = TaxSerializer()
    
    class Meta:
        model = ServiceType
        fields = '__all__'

# Invoice Item Serializer
class InvoiceItemSerializer(serializers.ModelSerializer):
    service_type = ServiceTypeSerializer()

    class Meta:
        model = InvoiceItem
        fields = '__all__'

# Invoice Serializer
class InvoiceSerializer(serializers.ModelSerializer):
    payment_method = PaymentMethodSerializer()
    student = StudentSerializer()
    invoice_items = InvoiceItemSerializer(source='invoiceitem_set', many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'