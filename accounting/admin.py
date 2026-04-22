from django.contrib import admin

# models
from .models import Account, JournalEntry, JournalEntryLine

admin.site.register(Account)
admin.site.register(JournalEntry)
admin.site.register(JournalEntryLine)