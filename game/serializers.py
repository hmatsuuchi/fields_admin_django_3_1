from rest_framework import serializers
# models
from attendance.models import Attendance, AttendanceRecord


# Attendance Serializer
class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ['date']

# Attendance Record Serializer
class AttendanceRecordSerializer(serializers.ModelSerializer):
    attendance = AttendanceSerializer(many=True, source='attendance_reverse_relationship')

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'status', 'attendance']