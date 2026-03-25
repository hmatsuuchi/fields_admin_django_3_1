from rest_framework import serializers
# models
from analytics.models import AtRiskStudents
from students.models import Students
from schedule.models import Events
from attendance.models import Attendance, AttendanceRecord
from django.contrib.auth.models import User

from user_profiles.models import UserProfilesInstructors

# ======= DASHBOARD WIDGET =======

# ======= Student Serializer =======
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['id', 'last_name_romaji', 'first_name_romaji', 'last_name_kanji', 'first_name_kanji', 'last_name_katakana', 'first_name_katakana']

# ======= At Risk Student List Serializer =======
class AtRiskStudentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False, read_only=True)

    class Meta:
        model = AtRiskStudents
        fields = '__all__'

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

# ====================================================================
# ======= OVERVIEW - INCOMPLETE ATTENDANCE FOR ALL INSTRUCTORS =======
# ====================================================================

# ======= User Profiles Instructors Serializer =======
class UserProfilesInstructorsSerializerForIAFAI(serializers.ModelSerializer):
    class Meta:
        model = UserProfilesInstructors
        fields = ['last_name_romaji', 'first_name_romaji']

# ======= Instructor Serializer =======
class InstructorSerializerForIAFAI(serializers.ModelSerializer):
    user_profiles_instructors = UserProfilesInstructorsSerializerForIAFAI(source="userprofilesinstructors", read_only=True)

    class Meta:
        model = User
        fields = ['id', 'user_profiles_instructors']

class AttendanceRecordsSerializerForIAFAI(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ['id']

# ======= Attendance Serializer =======
class AttendanceSerializerForIAFAI(serializers.ModelSerializer):
    instructor = InstructorSerializerForIAFAI(read_only=True)
    attendance_records = AttendanceRecordsSerializerForIAFAI(many=True, read_only=True)

    incomplete_count = serializers.IntegerField(read_only=True)
    complete_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id',
            'instructor',
            'date',
            'start_time',
            'attendance_records',
            'complete_count',
            'incomplete_count',
            ]