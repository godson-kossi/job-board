# Generated by Django 5.1.1 on 2024-10-17 08:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_application_applicant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='applicant',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.applicant'),
        ),
        migrations.AlterField(
            model_name='application',
            name='unidentified_applicant',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.unidentifiedapplicant'),
        ),
    ]
