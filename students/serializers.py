from rest_framework import serializers
from .models import Students, Phone

class PhoneSerializer(serializers.ModelSerializer):
    number_type_verbose = serializers.SerializerMethodField()

    class Meta:
        model = Phone
        fields = '__all__'

    def get_number_type_verbose(self, obj):
        try:
            return obj.number_type.name
        except:
            return ''

class ProfileSerializer(serializers.ModelSerializer):
    prefecture_verbose = serializers.SerializerMethodField()
    grade_verbose = serializers.SerializerMethodField()
    status_verbose = serializers.SerializerMethodField()
    payment_method_verbose = serializers.SerializerMethodField()
    grade_verbose = serializers.SerializerMethodField()
    status_verbose = serializers.SerializerMethodField()
    prefecture_verbose = serializers.SerializerMethodField()
    age = serializers.ReadOnlyField()

    phone = PhoneSerializer(many=True)

    class Meta:
        model = Students
        fields = '__all__'

    def get_prefecture_verbose(self, obj):
        try:
            return obj.prefecture.name
        except:
            return ''
    
    def get_grade_verbose(self, obj):
        try:
            return obj.grade.name
        except:
            return ''
    
    def get_status_verbose(self, obj):
        try:
            return obj.status.name
        except:
            return ''
    
    def get_payment_method_verbose(self, obj):
        try:
            return obj.payment_method.name
        except:
            return ''
        
    def get_grade_verbose(self, obj):
        try:
            return obj.grade.name
        except:
            return ''
        
    def get_status_verbose(self, obj):
        try:
            return obj.status.name
        except:
            return ''
        
    def get_prefecture_verbose(self, obj):
        try:
            return obj.prefecture.name
        except:
            return ''