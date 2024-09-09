from django.contrib import admin
from .models import Attendance, AttendanceRecord, AttendanceRecordStatus

admin.site.register(Attendance)
admin.site.register(AttendanceRecord)
admin.site.register(AttendanceRecordStatus)