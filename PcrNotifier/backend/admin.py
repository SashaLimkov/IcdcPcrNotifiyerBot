from django.contrib import admin

from backend.models import *


class EmployeeInline(admin.TabularInline):
    verbose_name = "Сотрудники"
    verbose_name_plural = "Сотрудники"
    model = Employee
    fields = ["name", "role"]
    readonly_fields = fields
    ordering = ("role",)
    show_change_link = True
    can_delete = False
    extra = 0


class OpenNotesInline(admin.TabularInline):
    verbose_name = "Открытая запись"
    verbose_name_plural = "Открытые записи"
    model = Note
    fields = ["employee", "patient_id", "datetime_get", "datetime_fill", "deadline_lost"]
    readonly_fields = ["patient_id", "datetime_get", "datetime_fill", "deadline_lost"]
    show_change_link = True
    can_delete = False
    extra = 0


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "_pretty_info")
    list_display_links = ("name",)

    def _pretty_info(self, item):
        return item.pretty_info

    _pretty_info.short_description = "Руководитель"
    inlines = (EmployeeInline,)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "_pretty_department")
    list_display_links = ("name",)

    def _pretty_department(self, item):
        return item.pretty_department

    _pretty_department.short_description = "Отдел"
    ordering = ("department", "role")
    inlines = (OpenNotesInline,)


class NoteAdmin(admin.ModelAdmin):
    list_display = ("_pretty_name", "deadline_lost")
    list_display_links = ("_pretty_name")

    def _pretty_name(self, item):
        return item.pretty_name

    _pretty_name.short_description = "Роль"


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Note)
admin.site.register(Role)
