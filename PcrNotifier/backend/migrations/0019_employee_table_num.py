# Generated by Django 4.2 on 2023-04-13 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_department_nsi_frmo'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='table_num',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='Табельный номер'),
        ),
    ]