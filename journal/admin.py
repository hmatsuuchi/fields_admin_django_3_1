from django.contrib import admin
from .models import Journal, JournalType

admin.site.register(Journal)
admin.site.register(JournalType)