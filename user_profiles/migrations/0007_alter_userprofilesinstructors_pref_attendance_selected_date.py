# Generated by Django 5.0.1 on 2024-10-16 23:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0006_userprofilesinstructors_pref_attendance_selected_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilesinstructors',
            name='pref_attendance_selected_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
