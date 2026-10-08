from django.contrib import admin
from .models import Attendance, AttendanceRecord, AttendanceRecordStatus, AttendanceRecordLessonNote, AttendanceRecordHomeworkNote, AttendanceRecordStudentNote

admin.site.register(Attendance)
admin.site.register(AttendanceRecord)
admin.site.register(AttendanceRecordStatus)
admin.site.register(AttendanceRecordLessonNote)
admin.site.register(AttendanceRecordHomeworkNote)
admin.site.register(AttendanceRecordStudentNote)