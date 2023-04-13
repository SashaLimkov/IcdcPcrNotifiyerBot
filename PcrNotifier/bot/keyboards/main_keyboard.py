from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from backend.models import Role


async def get_statistics(role: Role):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if role.name in ["ЗГД", "Эпидемиолог"]:
        keyboard.add(
            KeyboardButton(text="Краткая сводка по больнице")
        )
        keyboard.add(
            KeyboardButton(text="Статистика по отделам")
        )
        keyboard.add(
            KeyboardButton(text="Просрочки по отделам")
        )
        # keyboard.add(
        #     KeyboardButton(text="Статистика по пользователям")
        # )
    else:
        keyboard.add(
            KeyboardButton(text="Статистика")
        )
    return keyboard
