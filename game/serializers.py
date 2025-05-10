from rest_framework import serializers
# models
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

# ======= ALL PRESENT ATTENDANCE RECORDS FOR CURRENT DAY SERIALIZERS =======

# Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['id', 'first_name_romaji']

# Attendance Record Serializer
class AllPresentAttendanceRecordsForCurrentDaySerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False)
    present_attendance_records_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student', 'present_attendance_records_count']