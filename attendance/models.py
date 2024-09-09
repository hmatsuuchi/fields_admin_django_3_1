from django.db import models
# models
from schedule.models import Events
from students.models import Students
from django.contrib.auth.models import User

# attendance record
class Attendance(models.Model):
    linked_class        = models.ForeignKey(Events, on_delete=models.CASCADE, blank=False, null=False)
    instructor          = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    attendance_records  = models.ManyToManyField('AttendanceRecord', blank=True)

    date                = models.DateField(blank=False, null=False)
    start_time          = models.TimeField(blank=False, null=False)

    class Meta:
        verbose_name_plural = "Attendance"

    def __str__(self):
        return str(self.id) + " - " + str(self.date)
    
# attendance records for students
class AttendanceRecord(models.Model):
    student             = models.ForeignKey(Students, on_delete=models.CASCADE, blank=False, null=False)
    status              = models.ForeignKey('AttendanceRecordStatus', on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Attendance Records"

    def __str__(self):
        return str(self.id) + " - " + str(self.student) + " - " + str(self.status)

# attendance record status choices
class AttendanceRecordStatus(models.Model):
    status_name         = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Attendance Record Status"

    def __str__(self):
        return str(self.id) + " - " + str(self.status_name)