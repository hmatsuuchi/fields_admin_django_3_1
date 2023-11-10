from rest_framework import serializers
from django.contrib.auth.models import User

class LoggedInUserDataSerializer(serializers.ModelSerializer):
    def get_groups(self, obj):
        return obj.groups.values_list('name', flat=True)

    class Meta:
        model = User
        fields = ['username']