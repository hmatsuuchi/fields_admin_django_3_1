from rest_framework import serializers
from .models import Students, Phone

class PhoneSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    number_type_verbose = serializers.ReadOnlyField()

    class Meta:
        model = Phone
        fields = '__all__'
    
class ProfileSerializer(serializers.ModelSerializer):
    profile_full_name = serializers.ReadOnlyField()
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
    
    def update(self, instance, validated_data):
        # get nested phone data from the request
        phones_data = validated_data.pop('phone')

        # delete related phone records that are not in request phones_data
        phones_data_ids = [phones_data.get('id') for phones_data in phones_data if phones_data.get('id') is not None]
        related_phone_records_to_delete = instance.phone.all().exclude(id__in=phones_data_ids)
        related_phone_records_to_delete.delete()

        # update or create phone records that are in request phones_data
        for phone_data in phones_data:
            if phone_data.get('id') is None and phone_data['number'] != "":
                phone = Phone.objects.create(**phone_data)
                instance.phone.add(phone)
            elif phone_data.get('id') is not None and phone_data['number'] == "":
                phone = Phone.objects.get(id=phone_data['id'])
                phone.delete()
            else:
                phone = Phone.objects.update_or_create(id=phone_data['id'], defaults=phone_data)

        # update the other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
class ProfileSerializerForSelect(serializers.ModelSerializer):
    grade_verbose = serializers.ReadOnlyField()

    class Meta:
        model = Students
        fields = ['id', 'last_name_romaji', 'first_name_romaji', 'last_name_kanji', 'first_name_kanji', 'last_name_katakana', 'first_name_katakana', 'grade_verbose', 'status']