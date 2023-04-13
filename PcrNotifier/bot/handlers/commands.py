from aiogram import types
from aiogram.utils.deep_linking import decode_payload

from backend.services.employee import update_tg_by_pk, get_employee_by_tg, get_all_departments, \
    get_all_head_departments
from backend.services.notes import get_all_notes_count, count_of_not_filled, count_of_ill
from backend.tasks import try_send_message
from bot.data import text_data as td
from bot.keyboards import main_keyboard as kb


async def start_message(message: types.Message):
    args = message.get_args()
    telegram_id = message.chat.id
    if args:
        res = int(decode_payload(args))
        employee = update_tg_by_pk(e_pk=res, telegram_id=message.chat.id)
        if employee.telegram_id != telegram_id:
            await try_send_message(
                chat_id=telegram_id,
                text=td.ALREADY_AUTH
            )
    employee = get_employee_by_tg(telegram_id=telegram_id)
    if employee:
        await try_send_message(
            chat_id=telegram_id,
            text=td.WELCOME.format(name=employee.name),
            keyboard=await kb.get_statistics(role=employee.role)
        )


async def show_stat_by_role(message):
    telegram_id = message.chat.id
    employee = get_employee_by_tg(telegram_id=telegram_id)
    text = ""
    role = employee.role.name
    if role in ["ЗГД", "Эпидемиолог"]:
        for department in get_all_departments():
            text += td.STATISTICS[role].format(
                department=department.name,
                total_count=department.total_notes_count,
                lost_deadline_count=department.count_deadline_lost,
                not_filled=department.count_not_filled_notes,
                ill_count=department.ill_found_count
            )
    elif role == "Глава отдела":
        for department in get_all_head_departments(telegram_id=telegram_id):
            text += td.STATISTICS[role].format(
                department=department.name,
                total_count=department.total_notes_count,
                lost_deadline_count=department.count_deadline_lost,
                not_filled=department.count_not_filled_notes,
                ill_count=department.ill_found_count
            )
    else:
        text += td.STATISTICS[role].format(
            department=employee.department.name,
            total_count=employee.total_count,
            lost_deadline_count=employee.count_of_lost_deadline,
            not_filled=employee.not_filled_now,
            ill_count=employee.ill_found_count
        )
    await send_stat_messages(message=message, text=text)


async def total_stat_by_depart(message: types.Message):
    departments = get_all_departments()
    text = ""
    for dep in departments:
        total_count = dep.total_notes_count
        ill_count = dep.ill_found_count
        not_filled = dep.count_not_filled_notes
        text += "\n" + td.TOTAL_STAT["stat_by_depart"].format(total_count=total_count,
                                                              ill_count=ill_count,
                                                              not_filled=not_filled,
                                                              department=dep.name)
    await send_stat_messages(message=message, text=text)


async def show_short_stat(message: types.Message):
    text = td.TOTAL_STAT["total_stat"].format(
        total_count=get_all_notes_count(),
        not_filled=count_of_not_filled(),
        ill_count=count_of_ill(),
    )
    await send_stat_messages(message=message, text=text)


async def show_dep_lost_deadline_count(message: types.Message):
    text = ""
    departments = get_all_departments().order_by("-count_deadline_lost")
    for department in departments:
        text += td.TOTAL_STAT["stat_dep_lost_deadline"].format(department=department,
                                                               count=department.count_deadline_lost)

    await send_stat_messages(message=message, text=text)


async def send_stat_messages(message: types.Message, text: str):
    telegram_id = message.chat.id
    employee = get_employee_by_tg(telegram_id=telegram_id)
    keyboard = await kb.get_statistics(role=employee.role)
    await try_send_message(
        text=text,
        chat_id=telegram_id,
        keyboard=keyboard
    )
