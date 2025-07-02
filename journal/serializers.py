from rest_framework import serializers
# models
from django.contrib.auth.models import User
from .models import Journal, JournalType
from user_profiles.models import UserProfilesInstructors

# ======= JOURNAL FOR STUDENT PROFILE SERIALIZERS =======

# Journal Type Serializer
class JournalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalType
        fields = ['id', 'name']

# User Profile Instructor Serializer
class UserProfileInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfilesInstructors
        fields = [
            'last_name_kanji',
            'first_name_kanji',
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

# Journal Serializer for Details View
class GetJournalForProfileSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(required=False, many=True)
    type = JournalTypeSerializer(required=False)

    class Meta:
        model = Journal
        fields = ['id', 'date', 'time', 'type', 'instructor', 'text']