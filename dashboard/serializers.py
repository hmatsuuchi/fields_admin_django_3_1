from rest_framework import serializers
# models
from invoices.models import Invoice, InvoiceItem
from students.models import Students
from schedule.models import Events

# ==================================
# ======= UPCOMING BIRTHDAYS =======
# ==================================

# ======= Event Serializer =======
class EventSerializerForUpcomingBirthdays(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'primary_instructor', 'event_name', 'day_of_week', 'start_time', 'archived']

# ======= Student Serializer =======
class UpcomingBirthdayStudentSerializer(serializers.ModelSerializer):
    events_set = EventSerializerForUpcomingBirthdays(many=True, read_only=True)

    class Meta:
        model = Students
        fields = ['id', 'last_name_kanji', 'first_name_kanji', 'last_name_katakana', 'first_name_katakana', 'last_name_romaji', 'first_name_romaji', 'birthday', 'age', 'events_set']

# =====================================
# ======= INVOICES FOR CUSTOMER =======
# =====================================

# ======= Invoice Item Serializer =======
class InvoiceItemSerializer(serializers.ModelSerializer):
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    tax_type_name = serializers.CharField(source='service_type.tax.name', read_only=True)

    class Meta:
        model = InvoiceItem
        fields = '__all__'

# ======= Invoice Serializer =======
class InvoiceSerializerForCustomer(serializers.ModelSerializer):
    payment_method_name = serializers.CharField(source='payment_method.name', read_only=True)
    invoiceitem_set = InvoiceItemSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'