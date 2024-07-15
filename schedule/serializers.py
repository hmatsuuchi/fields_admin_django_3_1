from rest_framework import serializers
# models
from .models import Events, EventType
from students.models import Students
from user_profiles.models import UserProfilesInstructors
from django.contrib.auth.models import User

# Student Serializer
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

# Event Type Serializer
class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['id', 'name', 'duration', 'capacity']

# User Profile Instructor Serializer
class UserProfileInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfilesInstructors
        fields = '__all__'

# Instructor Serializer
class InstructorSerializer(serializers.ModelSerializer):
    userprofilesinstructors = UserProfileInstructorSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'userprofilesinstructors', 'username']

# Event Serializer
class EventsSerializer(serializers.ModelSerializer):
    students = StudentsSerializer(many=True, required=False)
    event_type = EventTypeSerializer(required=False)

    class Meta:
        model = Events
        fields = '__all__'

# Event Create Serializer
class EventCreateSerialzizer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'