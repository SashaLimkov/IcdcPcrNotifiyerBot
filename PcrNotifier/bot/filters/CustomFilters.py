from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from backend.services import employee


class NotEmployee(BoundFilter):
    async def check(self, message: types.Message | types.CallbackQuery) -> bool:
        match type(message):
            case types.Message:
                user_id = message.from_user.id
                user_profile = employee.get_employee_by_tg(user_id)
                return user_profile.role.name in ["ЗГД", "Эпидемиолог"]
            case _:
                return False
