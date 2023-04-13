from ninja import NinjaAPI, Schema

from api.routers import notes_router, employee_router, department_router

api = NinjaAPI()

api.add_router("/notes/", notes_router)
api.add_router("/employee/", employee_router)
api.add_router("/department/", department_router)
