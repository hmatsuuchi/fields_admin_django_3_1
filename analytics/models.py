from django.db import models

# stores highest active student count data
class HighestActiveStudentCount(models.Model):
    active_student_count        = models.PositiveIntegerField()

    date_time_created           = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified          = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Highest Active Student Count"
        verbose_name_plural = "Highest Active Student Counts"

    def __str__(self):
        return f"{self.date_time_created} [{self.active_student_count}]"
    
# stores highest revenue per student data
class HighestRevenuePerStudent(models.Model):
    revenue_per_student         = models.FloatField()
    value_type                  = models.CharField(max_length=10, choices=[('mean', 'Mean'), ('median', 'Median')], blank=False, null=False)

    date_time_created           = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified          = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Highest Revenue Per Student"
        verbose_name_plural = "Highest Revenue Per Student"

    def __str__(self):
        return f"{self.date_time_created} [{self.revenue_per_student:.2f}] ({self.value_type})"
    
# stores highest lifetime in days per student data
class HighestLifetimeInDaysPerStudent(models.Model):
    lifetime_in_days_per_student    = models.FloatField()
    value_type                      = models.CharField(max_length=10, choices=[('mean', 'Mean'), ('median', 'Median')], blank=False, null=False)

    date_time_created               = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified              = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Highest Lifetime In Days Per Student"
        verbose_name_plural = "Highest Lifetime In Days Per Student"

    def __str__(self):
        return f"{self.date_time_created} [{self.lifetime_in_days_per_student:.2f}] ({self.value_type})"
    
# stores a history of student churn model training
class StudentChurnModelTrainingHistory(models.Model):
    model_name                              = models.CharField(max_length=255, blank=False, null=False)

    notes                                   = models.TextField(blank=True, null=True)

    date_time_created                       = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_time_modified                      = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Student Churn Model Training History"
        verbose_name_plural = "Student Churn Model Training History"

    def __str__(self):
        return f"{self.id} - {self.model_name} ({self.date_time_created.strftime('%y-%m-%d')} @ {self.date_time_created.strftime('%H:%M:%S')})"