from django.contrib import admin
from .models import HighestActiveStudentCount, AtRiskStudents, StudentChurnModelTrainingHistory

admin.site.register(HighestActiveStudentCount)
admin.site.register(AtRiskStudents)
admin.site.register(StudentChurnModelTrainingHistory)