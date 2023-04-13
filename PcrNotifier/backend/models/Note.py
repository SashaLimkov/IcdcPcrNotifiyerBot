import asyncio
import datetime

from asgiref.sync import sync_to_async
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.models import Employee
from backend.services.employee import get_epid, get_md
from backend.tasks import notify_only_employee, notify_about_ill
from bot.data.text_data import TRUE_COV


class Note(models.Model):
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    patient_id = models.CharField("ID Пациента")
    patient_name = models.CharField("Имя пациента", max_length=255, default="")
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name="employee_notes",
                                 verbose_name="Сотрудник")
    datetime_get = models.DateTimeField("Время забора", blank=True, null=True)
    datetime_fill = models.DateTimeField("Время заполнения в системе", default=None, null=True, blank=True)
    count_of_notify = models.IntegerField("Количество отправленных уведомлений", default=0)
    deadline_lost = models.BooleanField("Дэдлайн не просрочен", default=True)
    is_ill = models.BooleanField("Положительный результат", blank=True, null=True)
    notification = models.BooleanField("Уведомление о положительном результате", default=False)
    first_notification = models.BooleanField("Уведомление о постановке задачи", default=False)
    # objects = models.Manager()

    def __str__(self):
        return f"{self.employee.name} {self.patient_id}"

    def pretty_name(self):
        return self.__str__()


@receiver(post_save, sender=Note, dispatch_uid="Notify user")
def first_notify(sender, instance, **kwargs):
    if not instance.first_notification:
        instance.first_notification = True
        instance.save()
        asyncio.run(notify_only_employee(note=instance))
    if instance.is_ill and not instance.notification:
        instance.notification = True
        instance.save()
        epid = get_epid()
        md = get_md()
        patient_id = instance.patient_id
        patient_name = instance.patient_name
        datetime_get = instance.datetime_get
        text = TRUE_COV.format(
            patient_id=patient_id,
            patient_name=patient_name,
            datetime_get=datetime_get,
            employee_name=instance.employee.name,
        )
        # asyncio.run(notify_only_employee(note=instance))
        telegram_id_list = [person.telegram_id for person in
                            (*epid, md, instance.employee, instance.employee.department.head)]
        asyncio.run(notify_about_ill(text=text, telegram_id_list=telegram_id_list))


@receiver(post_save, sender=Note, dispatch_uid="update_lost_count")
def update_notes_count(sender, instance, **kwargs):
    user = instance.employee
    user_lost_notes = user.employee_notes.filter(deadline_lost=False).count()
    user.ill_found_count = user.employee_notes.filter(is_ill=True).count()
    user.count_of_lost_deadline = user_lost_notes
    user.total_count = user.employee_notes.count()
    user.not_filled_now = user.employee_notes.filter(datetime_fill=None).count()
    user.save()
