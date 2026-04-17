from django.db import models
# models
from attendance.models import Attendance

# attendance alerts
class AttendanceAlert(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, blank=False, null=False)

    warning_date            = models.DateField()
    warning_note            = models.TextField(blank=True, null=True)

    pending_date            = models.DateField(blank=True, null=True)
    pending_note            = models.TextField(blank=True, null=True)

    resolved_date           = models.DateField(blank=True, null=True)
    resolved_note           = models.TextField(blank=True, null=True)

    date_time_created       = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified      = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Attendance Alerts"

    def __str__(self):
        return str(self.id) + " - [" + str(self.attendance.date) + " @ " + str(self.attendance.start_time) + "]"
