from rest_framework import serializers
from .models import Students, Phone

class PhoneSerializer(serializers.ModelSerializer):
    number_type_verbose = serializers.ReadOnlyField()

    class Meta:
        model = Phone
        fields = '__all__'

        
class ProfileSerializer(serializers.ModelSerializer):
    prefecture_verbose = serializers.ReadOnlyField()
    grade_verbose = serializers.ReadOnlyField()
    status_verbose = serializers.ReadOnlyField()
    payment_method_verbose = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()

    phone = PhoneSerializer(many=True)

    class Meta:
        model = Students
        fields = '__all__'