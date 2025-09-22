from rest_framework import serializers
# models
from analytics.models import AtRiskStudents
from students.models import Students
from schedule.models import Events

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