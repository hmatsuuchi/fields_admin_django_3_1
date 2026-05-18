from django.contrib import admin
from .models import HighestActiveStudentCount, AtRiskStudents, StudentChurnModelTrainingHistory, HighestRevenuePerStudent, HighestLifetimeInDaysPerStudent

admin.site.register(HighestActiveStudentCount)
admin.site.register(AtRiskStudents)
admin.site.register(StudentChurnModelTrainingHistory)
admin.site.register(HighestRevenuePerStudent)
admin.site.register(HighestLifetimeInDaysPerStudent)