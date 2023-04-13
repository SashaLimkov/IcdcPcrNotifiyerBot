from django.shortcuts import get_object_or_404
from ninja import Router

from api.schema import EmployeeSchema, Error
from backend.models import Role, Employee, Department

employee_router = Router()


@employee_router.post("/")
def create_employee(request, payload: EmployeeSchema):
    payload_dict = payload.dict()
    name = payload_dict["name"]
    table_num = payload_dict["table_num"]
    nsi_frmo = payload_dict["nsi_frmo"]
    role = Role.objects.filter(name=payload_dict["role"]).first()
    department = Department.objects.filter(nsi_frmo=nsi_frmo).first()
    if department:
        created = Employee.objects.filter(table_num=table_num).first()
        if created:
            created.name = name
            created.role = role
            created.department = department
            created.save()
        else:
            created = Employee.objects.create(name=name, role=role, department=department, table_num=table_num)
        return {"name": name, "role": role.name, "nsi_frmo": nsi_frmo, "table_num": table_num}


@employee_router.get("/{employee_id}_invite_link")
def get_deeplink_by_id(request, employee_id):
    employee = get_object_or_404(Employee, table_num=employee_id)
    return employee.invite_link


@employee_router.put("/update/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeSchema):
    payload_dict = payload.dict()
    r = Employee.objects.filter(pk=employee_id).update(
        **payload_dict
    )
    return {"result": r}


@employee_router.delete("/{table_num}")
def delete_employee(request, table_num: int):
    employee = Employee.objects.filter(table_num=table_num).first()
    departments = employee.head_department.all()
    for department in departments:
        department.head = None
        department.save()
    employee.delete()
