from django.contrib import admin

# models
from .models import Account, JournalEntry, JournalEntryLine, JournalContact

admin.site.register(Account)
admin.site.register(JournalEntry)
admin.site.register(JournalEntryLine)
admin.site.register(JournalContact)