from django.db import models
from django.contrib.auth.models import User
from students.models import Students

class Events(models.Model):
    event_name                  = models.CharField(max_length=100)
    event_type                  = models.ForeignKey('EventType', on_delete=models.CASCADE, blank=False, null=False)
    primary_instructor          = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    day_of_week                 = models.IntegerField(blank=False, null=False)
    start_time                  = models.TimeField(blank=False, null=False)

    students                    = models.ManyToManyField(Students, blank=True)
    
    archived                    = models.BooleanField(default=False, db_index=True)

    date_time_created           = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified          = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        return f"{str(self.primary_instructor)} {str(self.day_of_week)} {str(self.start_time)} {str(self.event_name)} [{str(self.id)}]"

class EventType(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{str(self.name)} -  {str(self.price)} -  {str(self.duration)} - {str(self.order)}"