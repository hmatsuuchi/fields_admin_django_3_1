from rest_framework import serializers
from django.contrib.auth.models import User
# models
from .models import Attendance, AttendanceRecord
from students.models import Students, GradeChoices
from schedule.models import Events, EventType
from user_profiles.models import UserProfilesInstructors

# Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = [
            'id',
            'last_name_romaji',
            'first_name_romaji',
            'last_name_kanji',
            'first_name_kanji',
            'last_name_katakana',
            'first_name_katakana',
            'grade_verbose',
            'status',
        ]

# Attendance Record Serializer
class AttendanceRecordSerializer(serializers.ModelSerializer):
    student = StudentSerializer(required=False)

    class Meta:
        model = AttendanceRecord
        fields = '__all__'

# Event Type Serializer
class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = [
            'id',
            'duration',
            'capacity',
        ]

# Linked Class Serializer
class LinkedClassSerializer(serializers.ModelSerializer):
    event_type = EventTypeSerializer(required=False)

    class Meta:
        model = Events
        fields = [
            'id',
            'event_name',
            'event_type',
        ]

# User Profile Instructor Serializer
class UserProfileInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfilesInstructors
        fields = [
            'last_name_romaji',
            'first_name_romaji',
            'icon_stub',
        ]

# Instructor Serializer
class InstructorSerializer(serializers.ModelSerializer):
    userprofilesinstructors = UserProfileInstructorSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'userprofilesinstructors', 'username']

# Attendance Serializer
class AttendanceSerializer(serializers.ModelSerializer):
    linked_class = LinkedClassSerializer(required=False)
    attendance_records = AttendanceRecordSerializer(many=True, required=False)
    instructor = InstructorSerializer(required=False)

    class Meta:
        model = Attendance
        fields = '__all__'

# ======= ATTENDANCE CHOICE LIST SERIALIZERS =======

# Instructor Profile Choice List Serializer
class UserInstructorProfileChoiceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfilesInstructors
        fields = ['id', 'icon_stub', 'last_name_kanji', 'first_name_kanji']

# Instructor Choice List Serializer
class UserInstructorSerializer(serializers.ModelSerializer):
    userprofilesinstructors = UserInstructorProfileChoiceListSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'userprofilesinstructors']

# Instructor Preferences Serializer
class UserInstructorPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfilesInstructors
        fields = ['pref_attendance_selected_instructor', 'pref_attendance_selected_date',]

# ======= EVENTS CHOICE LIST SERIALIZERS =======

# Students for Events Choice List Serializer
class StudentsForEventsChoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = [
            'id',
            'last_name_romaji',
            'first_name_romaji',
            'last_name_katakana',
            'first_name_katakana',
            'last_name_kanji',
            'first_name_kanji',
            'grade',
            'grade_verbose',
            'status',
        ]

# Event Type For Events Choice List Serializer
class EventTypeForEventsChoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['name', 'capacity']

# Events Choice List Serializer
class EventsChoiceListSerializer(serializers.ModelSerializer):
    primary_instructor = InstructorSerializer(required=False)
    event_type = EventTypeForEventsChoiceListSerializer(required=False)
    students = StudentsForEventsChoiceListSerializer(many=True, required=False)

    class Meta:
        model = Events
        fields = '__all__'

# ======= STUDENT CHOICE LIST SERIALIZERS =======

# Student Choice Serializer
class StudentsChoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = [
            'id',
            'last_name_romaji',
            'first_name_romaji',
            'last_name_kanji',
            'first_name_kanji',
            'last_name_katakana',
            'first_name_katakana',
            'grade_verbose',
            'status',
        ]

# ======= ATTENDANCE DETAILS SERIALIZERS =======

# Attendance Record Serializer for Details View
class AttendanceRecordForDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'

# Attendance Details Serializer
class AttendanceDetailsSerializer(serializers.ModelSerializer):
    attendance_records = AttendanceRecordForDetailsSerializer(many=True, required=False)

    def create(self, validated_data):
        # extract attendance records data
        attendance_records_data = validated_data.pop('attendance_records')

        # create attendance
        attendance = Attendance.objects.create(**validated_data)

        # create attendance records and add to list
        new_attendance_records = []
        for attendance_record_data in attendance_records_data:
            attendance_record = AttendanceRecord.objects.create(**attendance_record_data)
            new_attendance_records.append(attendance_record)

        # add attendance records to attendance
        attendance.attendance_records.add(*new_attendance_records)

        return attendance

    class Meta:
        model = Attendance
        fields = '__all__'

# ======= ATTENDANCE RECORD DETAILS SERIALIZERS =======

# Attendance Record Details Serializer
class AttendanceRecordDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'

# ======= ATTENDANCE FOR PROFILE DETAILS PAGE SERIALIZERS =======

# event type serializer for use in the profile details page
class EventTypeForProfileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['id', 'duration']

# linked class serializer for use in the profile details page
class LinkedClassForProfileDetailsSerializer(serializers.ModelSerializer):
    event_type = EventTypeForProfileDetailsSerializer(required=False)

    class Meta:
        model = Events
        fields = ['id', 'event_name', 'event_type']

# grade choices serializer for use in the profile details page
class GradeChoicesForProfileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeChoices
        fields = ['id', 'name']

# user profile instructor serializer for use in the profile details page
class UserProfileInstructorForProfileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfilesInstructors
        fields = [
            'id',
            'last_name_kanji',
            'icon_stub',
        ]

# instructor serializer for use in the profile details page
class InstructorForProfileDetailsSerializer(serializers.ModelSerializer):
    userprofilesinstructors = UserProfileInstructorForProfileDetailsSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'userprofilesinstructors']

# attendance serializer for us in the profile details page
class AttendanceForProfileDetailsSerializer(serializers.ModelSerializer):
    linked_class = LinkedClassForProfileDetailsSerializer(required=False)
    instructor = InstructorForProfileDetailsSerializer(required=False)

    class Meta:
        model = Attendance
        fields = ['id', 'linked_class', 'instructor', 'date', 'start_time']

# attendance record serializer for use in the profile details page
class AttendanceRecordForProfileDetailsSerializer(serializers.ModelSerializer):
    attendance_reverse_relationship = AttendanceForProfileDetailsSerializer(
        many=True, read_only=True
    )
    grade = GradeChoicesForProfileDetailsSerializer(required=False)

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'status', 'grade', 'attendance_reverse_relationship']