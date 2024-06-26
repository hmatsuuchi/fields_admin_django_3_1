from rest_framework import serializers
# models
from .models import Events, EventType
from students.models import Students
from user_profiles.models import UserProfilesInstructors
from django.contrib.auth.models import User

# used to include additional student data in the EventsSerializer
class StudentsSerializer(serializers.ModelSerializer):
    profile_full_name = serializers.ReadOnlyField()

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
            'profile_full_name',
            'status',
            'grade_verbose',
            ]

# used to include additional class data in the EventsSerializer
class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['id', 'name', 'duration', 'capacity']

# used to include additional user data in the InstructorSerializer
class UserProfileInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfilesInstructors
        fields = '__all__'

# used to include additional instructor data in the response
class InstructorSerializer(serializers.ModelSerializer):
    userprofilesinstructors = UserProfileInstructorSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'userprofilesinstructors', 'username']

# event serializer
class EventsSerializer(serializers.ModelSerializer):
    students = StudentsSerializer(many=True, required=False)
    event_type = EventTypeSerializer(required=False)

    class Meta:
        model = Events
        fields = '__all__'