# Generated by Django 5.0.1 on 2024-01-22 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_app', '0005_alter_jobs_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='arquivo_final',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]