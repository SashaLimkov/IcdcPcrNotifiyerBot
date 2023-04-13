from asgiref.sync import sync_to_async

from backend.models import Employee, Department


def get_epid():
    return Employee.objects.filter(role__name="Эпидемиолог").all()


def get_md():
    return Employee.objects.filter(role__name="ЗГД").first()


def get_employee_by_pk(e_pk):
    return Employee.objects.filter(pk=e_pk).first()


def update_tg_by_pk(e_pk: int, telegram_id: int):
    employee = get_employee_by_pk(e_pk=e_pk)
    if not employee.telegram_id:
        employee.telegram_id = telegram_id
        employee.save()
    return employee


def get_employee_by_tg(telegram_id: int):
    return Employee.objects.filter(telegram_id=telegram_id).first()


def get_all_departments():
    return Department.objects.all()


def get_all_head_departments(telegram_id):
    user = get_employee_by_tg(telegram_id=telegram_id)
    return user.head_department.all()
