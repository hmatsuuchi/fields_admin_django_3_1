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
    # uses the PhoneSerializer to serialize the phone data for many-to-many field
    phone = PhoneSerializer(many=True, required=False)

    class Meta:
        model = Students
        fields = '__all__'

    def create(self, validated_data):
        # get the phone data from the request
        phones_data = validated_data.pop('phone')
        # create a new profile
        profile = Students.objects.create(**validated_data)

        # iterates through phone data, creates new database entry, and adds it to the profile
        for phone_data in phones_data:
            phone = Phone.objects.create(**phone_data)
            profile.phone.add(phone)
        
        return profile