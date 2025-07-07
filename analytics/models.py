from django.db import models
from students.models import Students

# stores highest active student count data
class HighestActiveStudentCount(models.Model):
    active_student_count        = models.PositiveIntegerField()

    date_time_created           = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified          = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Highest Active Student Count"
        verbose_name_plural = "Highest Active Student Counts"

    def __str__(self):
        return f"{self.date_time_created} [{self.active_student_count}]"
    
# stores list of students who are at risk of quitting
class AtRiskStudents(models.Model):
    student                     = models.ForeignKey(Students, on_delete=models.CASCADE, blank=False, null=False)

    date_time_created           = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified          = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "At Risk Student"
        verbose_name_plural = "At Risk Students"

    def __str__(self):
        return f"{self.student.last_name_romaji} {self.student.first_name_romaji} [{self.date_time_created}]"