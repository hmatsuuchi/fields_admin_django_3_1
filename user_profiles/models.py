from django.db import models
from django.contrib.auth.models import User

class UserProfilesInstructors(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    last_name_romaji    = models.CharField(max_length=35, blank=True, null=True)
    first_name_romaji   = models.CharField(max_length=35, blank=True, null=True)
    last_name_katakana  = models.CharField(max_length=35, blank=True, null=True)
    first_name_katakana = models.CharField(max_length=35, blank=True, null=True)
    last_name_kanji     = models.CharField(max_length=35, blank=True, null=True)
    first_name_kanji    = models.CharField(max_length=35, blank=True, null=True)

    icon_stub           = models.CharField(max_length=35, blank=True, null=True)

    def __str__(self):
        return f"{self.last_name_romaji} {self.first_name_romaji} [{self.id}]"