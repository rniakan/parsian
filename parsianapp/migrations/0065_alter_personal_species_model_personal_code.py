# Generated by Django 3.2.15 on 2022-12-10 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsianapp', '0064_alter_personal_species_model_personal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal_species_model',
            name='personal_code',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
