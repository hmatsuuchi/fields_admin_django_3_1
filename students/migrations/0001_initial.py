# Generated by Django 4.2.4 on 2023-08-27 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GradeChoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('order', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Grade Choices',
            },
        ),
        migrations.CreateModel(
            name='PaymentChoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('order', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Payment Choices',
            },
        ),
        migrations.CreateModel(
            name='PrefectureChoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('order', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Prefecture Choices',
            },
        ),
        migrations.CreateModel(
            name='StatusChoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('order', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Status Choices',
            },
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name_romaji', models.CharField(max_length=35)),
                ('first_name_romaji', models.CharField(max_length=35)),
                ('last_name_kanji', models.CharField(max_length=35)),
                ('first_name_kanji', models.CharField(max_length=35)),
                ('last_name_katakana', models.CharField(max_length=35)),
                ('first_name_katakana', models.CharField(max_length=35)),
                ('post_code', models.CharField(blank=True, max_length=10)),
                ('city', models.CharField(blank=True, max_length=35)),
                ('address_1', models.CharField(blank=True, max_length=35)),
                ('address_2', models.CharField(blank=True, max_length=35)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('archived', models.BooleanField(default=False)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.gradechoices')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.paymentchoices')),
                ('prefecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.prefecturechoices')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.statuschoices')),
            ],
            options={
                'verbose_name_plural': 'Students',
            },
        ),
    ]
