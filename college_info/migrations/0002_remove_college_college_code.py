# Generated by Django 4.2 on 2025-04-03 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('college_info', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='college',
            name='college_code',
        ),
    ]
