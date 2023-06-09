# Generated by Django 4.2 on 2023-04-07 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_employee_options_note_count_of_notify_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='count_of_lost_deadline',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='total_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='telegram_id',
            field=models.BigIntegerField(blank=True, default=0, verbose_name='ID пользователя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='note',
            name='patient_name',
            field=models.CharField(default='', max_length=255, verbose_name='Имя пациента'),
        ),
        migrations.AlterField(
            model_name='note',
            name='datetime_fill',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время заполнения в системе'),
        ),
    ]
