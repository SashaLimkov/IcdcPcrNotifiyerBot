# Generated by Django 4.2 on 2023-04-11 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_note_is_ill'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='ill_found_count',
            field=models.IntegerField(default=0, verbose_name='Количество подтвержденных результатов'),
        ),
        migrations.AddField(
            model_name='employee',
            name='ill_found_count',
            field=models.IntegerField(default=0, verbose_name='Количество подтвержденных результатов'),
        ),
    ]