import traceback
from pprint import pprint

from ninja import Router

from api.schema import DepartmentSchema, Error
from backend.models import Department, Employee, Role

department_router = Router()


@department_router.post("/", response={201: DepartmentSchema})
def create_department(request, payload: DepartmentSchema):
    payload_dict = payload.dict()
    name = payload_dict.get("name")
    nsi_frmo = payload_dict.get("nsi_frmo")
    head_id = payload_dict.get("head_id")
    head = Employee.objects.filter(table_num=head_id).first()
    if not head:
        role = Role.objects.get(name="Глава отдела")
        head = Employee.objects.create(table_num=head_id, role=role)
    r = Department.objects.create(name=name, nsi_frmo=nsi_frmo, head=head)
    head.department = r
    head.save()
    return 201, r


@department_router.put("/{nsi_frmo}", response={200: DepartmentSchema, 404: Error})
def update_department(request, nsi_frmo: str, payload: DepartmentSchema):
    try:
        payload_dict = payload.dict()
        department = Department.objects.get(nsi_frmo=nsi_frmo)
        name = payload_dict.get("name")
        nsi_frmo = payload_dict.get("nsi_frmo")
        head_id = payload_dict.get("head_id")
        head = Employee.objects.filter(table_num=head_id).first()
        if head:
            department.name = name
            department.nsi_frmo = nsi_frmo
            department.head = head
            print(department)
            department.save()
            return 200, department
        else:
            return 404, {"message": f"No such deployee {head_id}"}
    except Exception as e:
        return 404, {"message": e}


@department_router.delete("/{nsi_frmo}", response={200: None, 404: Error})
def delete_department(request, nsi_frmo: str):
    try:
        department = Department.objects.get(nsi_frmo=nsi_frmo)
        employeers = department.department_employers.all()
        for employee in employeers:
            employee.department = None
            employee.save()
        department.delete()
        return 200
    except Exception as e:
        return 404, {"message": traceback.format_exc()}
