from django.contrib import admin
from .models import HighestActiveStudentCount, AtRiskStudents

admin.site.register(HighestActiveStudentCount)
admin.site.register(AtRiskStudents)