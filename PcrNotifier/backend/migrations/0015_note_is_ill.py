# Generated by Django 4.2 on 2023-04-11 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_department_count_not_filled_notes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='is_ill',
            field=models.BooleanField(blank=True, null=True, verbose_name='Положительный результат'),
        ),
    ]
