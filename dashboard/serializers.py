from rest_framework import serializers
# models
from analytics.models import AtRiskStudents
from students.models import Students

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
