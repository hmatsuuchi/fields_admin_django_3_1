# Generated by Django 5.0.1 on 2024-05-08 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0002_rename_userprofiles_userprofilesinstructors'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofilesinstructors',
            name='icon_stub',
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
    ]