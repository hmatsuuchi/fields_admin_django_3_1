from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

class Phone(models.Model):
    number                      = models.CharField(max_length=24, blank=True, null=True)
    number_type                 = models.ForeignKey("PhoneChoice", on_delete=models.CASCADE, blank=True, null=True)

    def number_type_verbose(self):
        try:
            return self.number_type.name
        except:
            return ''

    class Meta:
            verbose_name_plural = "Phone"

    def __str__(self):
        return f"{self.number} [{self.number_type}]"

class PhoneChoice(models.Model):
    name                        = models.CharField(max_length=35)
    order                       = models.IntegerField()

    class Meta:
        verbose_name_plural = "Phone Choices"

    def __str__(self):
        return f"{self.name} [{self.order}]"

class Students(models.Model):
    last_name_romaji            = models.CharField(max_length=35, blank=True, null=True)
    first_name_romaji           = models.CharField(max_length=35, blank=True, null=True)
    last_name_kanji             = models.CharField(max_length=35, blank=True, null=True)
    first_name_kanji            = models.CharField(max_length=35, blank=True, null=True)
    last_name_katakana          = models.CharField(max_length=35, blank=True, null=True)
    first_name_katakana         = models.CharField(max_length=35, blank=True, null=True)

    post_code                   = models.CharField(max_length=10, blank=True, null=True)
    prefecture                  = models.ForeignKey("PrefectureChoices", on_delete=models.CASCADE, blank=True, null=True)
    city                        = models.CharField(max_length=35, blank=True, null=True)
    address_1                   = models.CharField(max_length=35, blank=True, null=True)
    address_2                   = models.CharField(max_length=35, blank=True, null=True)

    phone                       = models.ManyToManyField(Phone, blank=True)

    birthday                    = models.DateField(null=True, blank=True)
    grade                       = models.ForeignKey("GradeChoices", on_delete=models.CASCADE, blank=True, null=True)

    status                      = models.ForeignKey("StatusChoices", on_delete=models.CASCADE, blank=True, null=True)

    payment_method              = models.ForeignKey("PaymentChoices", on_delete=models.CASCADE, blank=True, null=True)

    archived                    = models.BooleanField(default=False)

    date_time_created           = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified          = models.DateTimeField(auto_now=True, blank=True, null=True)

    @cached_property
    def prefecture_verbose(self):
        try:
            return self.prefecture.name
        except:
            return ''
        
    @cached_property
    def grade_verbose(self):
        try:
            return self.grade.name
        except:
            return ''
        
    @cached_property
    def status_verbose(self):
        try:
            return self.status.name
        except:
            return ''
        
    @cached_property
    def payment_method_verbose(self):
        try:
            return self.payment_method.name
        except:
            return ''

    @cached_property
    def age(self):
        if self.birthday:
            now = timezone.now()
            birthday = self.birthday

            age = now.year - birthday.year - ((now.month, now.day) < (birthday.month, birthday.day))
        else:
            age = ""

        return str(age)

    class Meta:
        verbose_name_plural = "Students"

    def __str__(self):
        return str(self.id)

class PrefectureChoices(models.Model):
    name                        = models.CharField(max_length=35)
    order                       = models.IntegerField()

    class Meta:
        verbose_name_plural = "Prefecture Choices"

    def __str__(self):
        return f"{self.name} [{self.order}]"

class GradeChoices(models.Model):
    name                        = models.CharField(max_length=35)
    order                       = models.IntegerField()

    class Meta:
        verbose_name_plural = "Grade Choices"

    def __str__(self):
        return f"{self.name} [{self.order}]"

class StatusChoices(models.Model):
    name                        = models.CharField(max_length=35)
    order                       = models.IntegerField()

    class Meta:
        verbose_name_plural = "Status Choices"

    def __str__(self):
        return f"{self.name} [{self.order}]"

class PaymentChoices(models.Model):
    name                        = models.CharField(max_length=35)
    order                       = models.IntegerField()

    class Meta:
        verbose_name_plural = "Payment Choices"

    def __str__(self):
        return f"{self.name} [{self.order}]"
    