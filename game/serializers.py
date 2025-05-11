from rest_framework import serializers
# models
from .models import CheckIn
from attendance.models import Attendance, AttendanceRecord
from students.models import Students

# ======= STUDENT DETAILS SERIALIZERS =======

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

# ======= RECENT CHECKINS SERIALIZERS =======

# Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['id', 'first_name_romaji']

# Checkin Serializer
class CheckInSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False)

    class Meta:
        model = CheckIn
        fields = ['id', 'student', 'date_time_created', 'attendance_present_count']