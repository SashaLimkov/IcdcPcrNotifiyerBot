# Generated by Django 4.2 on 2023-04-13 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0021_alter_employee_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='patient_id',
            field=models.CharField(verbose_name='ID Пациента'),
        ),
    ]
