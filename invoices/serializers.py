from rest_framework import serializers
# MODELS
from .models import Invoice, PaymentMethod, InvoiceItem, ServiceType, Tax
from students.models import Students


# ========== INVOICE LIST ALL SERIALIZER ==========

# Payment Method Serializer
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name',]

# Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['id', 'last_name_kanji', 'first_name_kanji',]

# Tax Serializer
class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ['id', 'name', 'rate',]

# Service Type Serializer
class ServiceTypeSerializer(serializers.ModelSerializer):
    tax = TaxSerializer()
    
    class Meta:
        model = ServiceType
        fields = ['id', 'name', 'price', 'tax',]

# Invoice Item Serializer
class InvoiceItemSerializer(serializers.ModelSerializer):
    service_type = ServiceTypeSerializer()

    class Meta:
        model = InvoiceItem
        fields = ['id', 'description', 'quantity', 'rate', 'tax', 'service_type',]

# Invoice Serializer
class InvoiceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    payment_method = PaymentMethodSerializer()
    invoice_items = InvoiceItemSerializer(source='invoiceitem_set', many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'customer_name',
            'customer_postal_code',
            'customer_prefecture',
            'customer_city',
            'customer_address_line_1',
            'customer_address_line_2',
            'year',
            'month',
            'transfer_date',
            'issued',
            'paid',
            'student',
            'payment_method',
            'invoice_items',
            'date_time_created',
            'date_time_modified',
            ]
        
# ========== PROFILE  SERIALIZER ==========

class ProfilesListForSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = [
            'id',
            'last_name_kanji',
            'first_name_kanji',
            'last_name_romaji',
            'first_name_romaji',
            'last_name_katakana',
            'first_name_katakana',
            'grade_verbose',
            'post_code',
            'prefecture_verbose',
            'city',
            'address_1',
            'address_2',
            ]