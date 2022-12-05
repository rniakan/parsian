# Generated by Django 4.0 on 2022-08-07 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsianapp', '0036_para_clinic_model_opto_date_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinations_model',
            name='blood_pressure',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examinations_model',
            name='length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examinations_model',
            name='pulse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examinations_model',
            name='weight',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='personal_species_model',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
