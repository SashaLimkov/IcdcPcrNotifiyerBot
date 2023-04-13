# Create your models here.
import datetime
from typing import Optional

from ninja import ModelSchema, Schema

from backend.models import Department, Employee


class EmployeeSchema(Schema):
    name: str = None
    role: str = "Сотрудник"
    nsi_frmo: str = None
    table_num: int


class DepartmentSchema(Schema):
    name: str
    nsi_frmo: str
    head_id: int


class DepartmentIn(Schema):
    name: str = None
    nsi_frmo = str
    head_id: int = None


class PathDate(Schema):
    year: int
    month: int
    day: int
    hour: int
    minute: int

    def value(self):
        return datetime.datetime(self.year, self.month, self.day, self.hour, self.minute)


class NoteIn(Schema):
    dspResultN: str
    patient_name: str
    employee_table_num: int
    datetime_get: PathDate


class CloseNote(Schema):
    dspResultN: str
    employee_table_num: str
    datetime_fill: PathDate
    is_ill: int


class Error(Schema):
    message: str
