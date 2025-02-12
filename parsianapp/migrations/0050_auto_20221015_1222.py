# Generated by Django 3.2.15 on 2022-10-15 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parsianapp', '0049_para_clinic_model_audio_l_three_ac_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinationscourse',
            name='company',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='parsianapp.company'),
        ),
        migrations.AlterField(
            model_name='personal_species_model',
            name='age',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='personal_species_model',
            name='examinations_code',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='parsianapp.examinationscourse'),
        ),
        migrations.AlterField(
            model_name='personal_species_model',
            name='gender',
            field=models.CharField(blank=True, choices=[('mard', 'مرد'), ('zan', 'زن')], default='mard', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='personal_species_model',
            name='marriage_status',
            field=models.CharField(blank=True, choices=[('mojarad', 'مجرد'), ('motahel', 'متاحل')], default='mojarad', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='personal_species_model',
            name='medical_exemption',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='personal_species_model',
            name='military_status',
            field=models.CharField(blank=True, choices=[('khedmat_karde', 'خدمت کرده'), ('moaf', 'معاف'), ('khedmat_nakarde', 'خدمت نکرده')], default='khedmat_karde', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='personal_species_model',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=250, null=True),
        ),
    ]
