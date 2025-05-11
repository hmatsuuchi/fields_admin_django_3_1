from django.db import models

from students.models import Students

# game ids
class CardUUID(models.Model):
    card_uuid           = models.CharField(max_length=255, unique=True)

    linked_student      = models.ForeignKey(Students, on_delete=models.CASCADE)

    date_time_created   = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified  = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Game Card UUIDs"

    def __str__(self):
        return str(self.id) + " - " + str(self.card_uuid) + " - " + str(self.linked_student)
    
# checkins
class CheckIn(models.Model):
    student                     = models.ForeignKey(Students, on_delete=models.CASCADE)
    attendance_present_count    = models.IntegerField(default=0)

    date_time_created           = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified          = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.id) + " - " + str(self.student) + " - " + str(self.attendance_present_count) + " - " + str(self.date_time_created)