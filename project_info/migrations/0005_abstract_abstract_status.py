# Generated by Django 4.2 on 2025-05-01 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_info', '0004_alter_project_reviews_project_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='abstract_status',
            field=models.CharField(blank=True, default='PENDING', max_length=16, null=True),
        ),
    ]
