# Generated by Django 4.2 on 2023-04-07 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_employee_count_of_lost_deadline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='telegram_id',
            field=models.BigIntegerField(blank=True, default=None, null=True, verbose_name='ID пользователя'),
        ),
    ]
