# Generated by Django 5.0.1 on 2024-07-15 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_alter_events_day_of_week_alter_events_event_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='archived',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
