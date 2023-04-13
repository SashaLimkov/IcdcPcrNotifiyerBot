from datetime import datetime

from django.shortcuts import get_object_or_404
from ninja import Router

from api.schema import NoteIn, PathDate, CloseNote
from backend.models import Employee, Note

notes_router = Router()


@notes_router.post("/")
def add_note(request, payload: NoteIn):
    payload_data = payload.dict()
    patient_id = payload_data.get("dspResultN")
    patient_name = payload_data.get("patient_name")
    employee_table_num = payload_data.get("employee_table_num")
    datetime_data = payload_data.get("datetime_get")
    datetime_get = datetime(
        datetime_data["year"],
        datetime_data["month"],
        datetime_data["day"],
        datetime_data["hour"],
        datetime_data["minute"])
    employee = Employee.objects.filter(table_num=employee_table_num).first()
    Note.objects.create(patient_name=patient_name,
                        patient_id=patient_id,
                        datetime_get=datetime_get,
                        employee=employee)
    return {
        "dspResultN": patient_id,
        "patient_name": patient_name,
        "employee_table_num": employee_table_num,
        "datetime_get": datetime_data,
    }


@notes_router.put("/")
def close_note(request, payload: CloseNote):
    payload_data = payload.dict()
    print(payload_data)
    patient_id = payload_data.get("dspResultN")
    employee_table_num = payload_data.get("employee_table_num")
    datetime_data = payload_data.get("datetime_fill")
    datetime_fill = datetime(
        datetime_data["year"],
        datetime_data["month"],
        datetime_data["day"],
        datetime_data["hour"],
        datetime_data["minute"])
    employee = Employee.objects.filter(table_num=employee_table_num).first()
    note = get_object_or_404(Note, employee=employee, patient_id=patient_id)
    if note:
        print(123, note)
        note.datetime_fill = datetime_fill
        note.is_ill = bool(payload_data["is_ill"])
        note.save()
        return {
            "dspResultN": patient_id,
            "employee_table_num": employee_table_num,
            "datetime_fill": datetime_data,
            "is_ill": bool(payload_data["is_ill"]),
        }
