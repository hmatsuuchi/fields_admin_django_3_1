from django.db import models
from django.contrib.auth.models import User
from students.models import Students
import datetime

class UserProfilesInstructors(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    last_name_romaji    = models.CharField(max_length=35, blank=True, null=True)
    first_name_romaji   = models.CharField(max_length=35, blank=True, null=True)
    last_name_katakana  = models.CharField(max_length=35, blank=True, null=True)
    first_name_katakana = models.CharField(max_length=35, blank=True, null=True)
    last_name_kanji     = models.CharField(max_length=35, blank=True, null=True)
    first_name_kanji    = models.CharField(max_length=35, blank=True, null=True)

    icon_stub           = models.CharField(max_length=35, blank=True, null=True)

    archived            = models.BooleanField(default=False)

    # PREFERENCES - DASHBOARD
    pref_dashboard_working_days = models.JSONField(default=list, blank=True, null=True)

    # PREFERENCES - ATTENDANCE
    pref_attendance_selected_instructor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='pref_attendance_selected_instructor')
    pref_attendance_selected_date       = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name_plural = "Instructors"

    def __str__(self):
        return f"{self.last_name_romaji} {self.first_name_romaji} [{self.id}]"
    
class UserProfilesCustomers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    last_name_romaji    = models.CharField(max_length=35, blank=True, null=True)
    last_name_katakana  = models.CharField(max_length=35, blank=True, null=True)
    last_name_kanji     = models.CharField(max_length=35, blank=True, null=True)

    related_students    = models.ManyToManyField(Students, blank=True, related_name='related_students')

    archived            = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Customers"

    def __str__(self):
        students = ", ".join(str(s.first_name_romaji) for s in self.related_students.all())
        return f" [{self.id}] {self.last_name_kanji} - {self.last_name_katakana} - {self.last_name_romaji} - {self.user.username} - ({students})"