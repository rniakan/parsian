# Generated by Django 4.0 on 2022-08-08 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsianapp', '0039_remove_job_history_model_current_job_from_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal_species_model',
            name='age',
            field=models.IntegerField(default=None),
        ),
    ]
