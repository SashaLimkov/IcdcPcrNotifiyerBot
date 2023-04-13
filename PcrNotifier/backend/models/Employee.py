from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from aiogram.utils.deep_linking import encode_payload

from backend.models import Role


class Employee(models.Model):
    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    telegram_id = models.BigIntegerField(verbose_name="ID пользователя", blank=True, null=True, default=None)
    name = models.CharField("ФИО", max_length=255, blank=True, null=True)
    role = models.ForeignKey(Role, to_field="name", default="Сотрудник", on_delete=models.DO_NOTHING,
                             verbose_name="Роль", related_name="employers")
    department = models.ForeignKey("Department", on_delete=models.DO_NOTHING, related_name="department_employers",
                                   verbose_name="Отдел", blank=True, null=True)
    table_num = models.IntegerField("Табельный номер", null=True, blank=True, unique=True)
    count_of_lost_deadline = models.IntegerField("Количество просрочек", default=0)
    not_filled_now = models.IntegerField("Количество не заполненных на данный момент", default=0)
    total_count = models.IntegerField("Всего записей", default=0)
    invite_link = models.CharField("Инвайт ссылка", max_length=128, default=None, null=True, blank=True)
    ill_found_count = models.IntegerField("Количество подтвержденных результатов", default=0)

    def __str__(self):
        return self.name if self.name else " "

    @property
    def pretty_role(self):
        return self.role.name

    @property
    def pretty_department(self):
        return mark_safe(
            f'<a href="/admin/backend/department/{self.department.pk}/change">{self.department.name}</a>') if self.department else "-"


@receiver(post_save, sender=Employee)
def update_invite_link(sender, instance, **kwargs):
    if not instance.invite_link:
        pk = instance.pk
        link = "https://t.me/icdc_pcr_notifier_bot?start="
        link += encode_payload(f"{pk}")
        instance.invite_link = link
        instance.save()
    department = instance.department
    if department:
        all_employers = Employee.objects.filter(department=department)
        dep_all_notes = all_employers.aggregate(Sum("total_count"))["total_count__sum"]
        dep_lost_notes = all_employers.aggregate(Sum("count_of_lost_deadline"))[
            "count_of_lost_deadline__sum"]
        not_filled = all_employers.aggregate(Sum("not_filled_now"))["not_filled_now__sum"]
        ill_found_count = all_employers.aggregate(Sum("ill_found_count"))["ill_found_count__sum"]
        department.count_deadline_lost = dep_lost_notes
        department.total_notes_count = dep_all_notes
        department.count_not_filled_notes = not_filled
        department.ill_found_count = ill_found_count
        department.save()
