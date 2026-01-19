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
        fields = ['id', 'last_name_kanji', 'first_name_kanji', 'payment_method_from_invoice',]

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

# Invoice Serializer
class InvoiceForInvoiceItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'customer_name', 'year', 'month',]

# Invoice Item Serializer
class InvoiceItemSerializer(serializers.ModelSerializer):
    invoice = InvoiceForInvoiceItemsSerializer()
    service_type = ServiceTypeSerializer()
    tax_type = TaxSerializer()


    class Meta:
        model = InvoiceItem
        fields = [
            'id',
            'description',
            'quantity',
            'rate',
            'tax_rate',
            'invoice',
            'service_type',
            'tax_type',
            'date_time_created',
            'date_time_modified',]

# Invoice List All Serializer
class InvoiceListAllSerializer(serializers.ModelSerializer):
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
            'creation_date',
            'transfer_date',
            'issued_date',
            'paid_date',
            'issued',
            'paid',
            'student',
            'payment_method',
            'invoice_items',
            'date_time_created',
            'date_time_modified',
            ]

# ========== INVOICE STATUS ALL SERIALIZER ==========
# Student Serializer for Invoice Status All Serializer
class StudentSerializerForInvoiceStatusAll(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['id', 'last_name_kanji', 'first_name_kanji', 'last_name_katakana', 'first_name_katakana', 'last_name_romaji', 'first_name_romaji',]

# Invoice Status All Serializer
class InvoiceStatusAllSerializer(serializers.ModelSerializer):
    student = StudentSerializerForInvoiceStatusAll()
    invoice_items = InvoiceItemSerializer(source='invoiceitem_set', many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'customer_name',
            'year',
            'month',
            'creation_date',
            'transfer_date',
            'issued_date',
            'paid_date',
            'issued',
            'paid',
            'student',
            'invoice_items',
            'date_time_created',
            'date_time_modified',
            ]

# ========== INVOICE CREATE SERIALIZER ==========
class InvoiceItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['description', 'quantity', 'rate', 'tax_rate', 'service_type', 'tax_type']

class InvoiceCreateSerializer(serializers.ModelSerializer):
    line_items = InvoiceItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Invoice
        fields = [
            'customer_name',
            'customer_postal_code',
            'customer_prefecture',
            'customer_city',
            'customer_address_line_1',
            'customer_address_line_2',
            'year',
            'month',
            'creation_date',
            'transfer_date',
            'issued',
            'paid',
            'student',
            'payment_method',
            'line_items',
            ]

    def create(self, validated_data):
        line_items_data = validated_data.pop('line_items')
        invoice = Invoice.objects.create(**validated_data)

        for line_item in line_items_data:
            InvoiceItem.objects.create(invoice=invoice, **line_item)
        
        return invoice

# ========== PROFILE SERIALIZER FOR SELECTION LIST ==========
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
            'payment_method_from_invoice',
            ]
        
# ========== PAYMENT METHOD SERIALIZER FOR SELECTION LIST ==========
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

# ========== SERVICE TYPE SERIALIZER FOR SELECTION LIST ==========
class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

# ========== TAX SERIALIZER FOR SELECTION LIST ==========
class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'