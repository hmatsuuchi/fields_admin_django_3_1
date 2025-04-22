from django.db import models

from students.models import Students

# game ids
class CardUUID (models.Model):
    card_uuid           = models.CharField(max_length=255, unique=True)

    linked_student      = models.ForeignKey(Students, on_delete=models.CASCADE)

    date_time_created   = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified  = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Game Card UUIDs"

    def __str__(self):
        return str(self.id) + " - " + str(self.card_uuid) + " - " + str(self.linked_student)