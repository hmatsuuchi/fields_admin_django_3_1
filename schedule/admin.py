from django.contrib import admin
from .models import Events, EventType, EventTypeFinancialProfile

admin.site.register(Events)
admin.site.register(EventType)
admin.site.register(EventTypeFinancialProfile)
