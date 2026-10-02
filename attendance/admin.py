from django.contrib import admin
from .models import Attendance, AttendanceRecord, AttendanceRecordStatus, AttendanceNote, AttendanceNoteComment

admin.site.register(Attendance)
admin.site.register(AttendanceRecord)
admin.site.register(AttendanceRecordStatus)
admin.site.register(AttendanceNote)
admin.site.register(AttendanceNoteComment)