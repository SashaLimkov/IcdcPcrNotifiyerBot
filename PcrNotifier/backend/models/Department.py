from django.db import models
from django.utils.safestring import mark_safe


class Department(models.Model):
    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"

    name = models.CharField("Название отдела", max_length=255)
    nsi_frmo = models.CharField("НСИ ФРМО", max_length=300, default="")
    head = models.ForeignKey("Employee", on_delete=models.DO_NOTHING, related_name="head_department", null=True,
                             blank=True, verbose_name="Глава отдела")
    total_notes_count = models.IntegerField("Количество всех записей", default=0)
    count_deadline_lost = models.IntegerField("Количество просрочек", default=0)
    count_not_filled_notes = models.IntegerField("Незаполненно на текущий момент", default=0)
    ill_found_count = models.IntegerField("Количество подтвержденных результатов", default=0)

    def __str__(self):
        return self.name

    @property
    def pretty_info(self):
        return mark_safe(
            f'<a href="/admin/backend/employee/{self.head.pk}/change">{self.head.name}</a>') if self.head else " "
