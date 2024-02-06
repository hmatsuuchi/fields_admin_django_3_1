from rest_framework import serializers
# models
from .models import Events, EventType
from students.models import Students
from django.contrib.auth.models import User

# used to include additional student data in the EventsSerializer
class StudentsSerializer(serializers.ModelSerializer):
    profile_full_name = serializers.ReadOnlyField()

    class Meta:
        model = Students
        fields = ['id', 'first_name_romaji', 'profile_full_name']

# used to include additional class data in the EventsSerializer
class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['id', 'name', 'duration']

# used to include additional instructor data in the response
class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class EventsSerializer(serializers.ModelSerializer):
    students = StudentsSerializer(many=True, required=False)
    event_type = EventTypeSerializer(required=False)

    class Meta:
        model = Events
        fields = '__all__'