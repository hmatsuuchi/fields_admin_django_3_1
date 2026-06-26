from django.contrib import admin
from .models import UserProfilesInstructors, UserProfilesCustomers

admin.site.register(UserProfilesInstructors)
admin.site.register(UserProfilesCustomers)