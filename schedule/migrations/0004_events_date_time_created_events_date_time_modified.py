# Generated by Django 5.0.1 on 2024-04-12 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_events_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='date_time_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='date_time_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]