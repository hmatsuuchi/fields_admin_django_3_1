from rest_framework import serializers
# models
from invoices.models import Invoice, InvoiceItem
from students.models import Students
from schedule.models import Events, EventType
from analytics.models import StudentChurnPrediction
from attendance.models import Attendance, AttendanceRecord

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

# ===============================================
# ======= ATTENDANCE RECORDS FOR CUSTOMER =======
# ===============================================
class EventTypeSerializerForCustomer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['id', 'name']

class LinkedClassSerializerForCustomer(serializers.ModelSerializer):
    event_type = EventTypeSerializerForCustomer(read_only=True)

    class Meta:
        model = Events
        fields = ['id', 'event_name', 'primary_instructor', 'start_time', 'event_type']

class AttendanceSerializerForCustomer(serializers.ModelSerializer):
    linked_class = LinkedClassSerializerForCustomer(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'linked_class', 'date']

class AttendanceRecordSerializerForCustomer(serializers.ModelSerializer):
    attendance_reverse_relationship = AttendanceSerializerForCustomer(many=True, read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student', 'status','attendance_reverse_relationship']

# ================================
# ======= AT RISK STUDENTS =======
# ================================

# ======= Student Serializer =======
class AtRiskStudentStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['id', 'last_name_kanji', 'first_name_kanji', 'last_name_katakana', 'first_name_katakana', 'last_name_romaji', 'first_name_romaji', 'age']

# ======= At Risk Student Serializer =======
class AtRiskStudentSerializer(serializers.ModelSerializer):
    student = AtRiskStudentStudentSerializer(read_only=True)
    
    class Meta:
        model = StudentChurnPrediction
        fields = '__all__'