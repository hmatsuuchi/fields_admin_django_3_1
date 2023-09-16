from django.contrib import admin
from .models import Students, PrefectureChoices, GradeChoices, StatusChoices, PaymentChoices, Phone, PhoneChoice

admin.site.register(Students)
admin.site.register(PrefectureChoices)
admin.site.register(GradeChoices)
admin.site.register(StatusChoices)
admin.site.register(PaymentChoices)
admin.site.register(Phone)
admin.site.register(PhoneChoice)