# Generated by Django 4.0 on 2022-07-01 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsianapp', '0010_final_theory_model_d_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='final_theory_model',
            name='d_code',
            field=models.IntegerField(blank=True, default='', null=True),
        ),
    ]
