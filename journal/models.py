from django.db import models
from students.models import Students
from django.contrib.auth.models import User

class Journal(models.Model):
    student         = models.ForeignKey(Students, on_delete=models.CASCADE)
    date            = models.DateField()
    time            = models.TimeField(null=True, blank=True)
    type            = models.ForeignKey('JournalType', on_delete=models.CASCADE)
    instructor      = models.ManyToManyField(User)
    text            = models.TextField(null=True, blank=True)

class JournalType(models.Model):
    name            = models.CharField(max_length=100)
    order           = models.IntegerField()

    class Meta:
        verbose_name_plural = "Journal Types"

    def __str__(self):
        return str(self.id) + " - " + str(self.name) + " [" + str(self.order) + "]"