import datetime
import traceback

from asgiref.sync import async_to_sync

from backend.models import Note, Employee
from backend.services.employee import get_epid, get_md
from backend.services.notes import get_all_notes, get_all_notes_count, count_of_not_filled, count_of_ill
from bot.config.loader import bot
from bot.data import text_data as td


async def notify_epid_and_md():
    text = td.TOTAL_STAT["total_stat"].format(
        total_count=get_all_notes_count(),
        not_filled=count_of_not_filled(),
        ill_count=count_of_ill(),
    )
    epid = get_epid()
    md = get_md()
    for person in (*epid, md):
        await try_send_message(
            chat_id=person.telegram_id,
            text=text
        )


async def notifier():
    notes_list = Note.Note.objects.all()
    for note in notes_list:
        if not note.datetime_fill:
            datetime_get = note.datetime_get
            now = datetime.datetime.now()
            diff = now - datetime_get
            hours_diff = diff.seconds / 60
            print(hours_diff)
            db_count = note.count_of_notify
            if 2.0 < hours_diff < 4.0:
                count = 1
            else:
                return
            if db_count != count:
                f = NOTIFY_BY_COUNT[count]
                result = await f(note=note)
                if result:
                    note.deadline_lost = False
                    note.count_of_notify += 1
                    note.save()


async def notify_only_employee(note: Note):
    patient_id = note.patient_id
    patient_name = note.patient_name
    text = td.ONLY_EMPLOYEE.format(patient_id=patient_id, patient_name=patient_name)
    await try_send_message(
        text=text,
        chat_id=note.employee.telegram_id
    )


# @async_to_sync
async def notify_about_ill(telegram_id_list, text):
    for telegram_id in telegram_id_list:
        await try_send_message(
            text=text,
            chat_id=telegram_id
        )


async def notify_employee_and_head(note: Note):
    patient_id = note.patient_id
    patient_name = note.patient_name
    datetime_get = note.datetime_get
    employee = note.employee
    head = employee.department.head
    employee_text = td.EMPLOYEE_AND_HEAD["employee"].format(
        patient_id=patient_id,
        patient_name=patient_name,
        datetime_get=datetime_get,
    )
    head_text = td.EMPLOYEE_AND_HEAD["head"].format(
        name=employee.name,
        patient_name=patient_name,
        patient_id=patient_id,
        datetime_get=datetime_get
    )
    await try_send_message(chat_id=employee.telegram_id, text=employee_text)
    await try_send_message(chat_id=head.telegram_id, text=head_text)
    return 1


# async def notify_epid(note: Note):


# async def notify_employee_head_epid_md(note: Note):
#     await notify_employee_and_head(note=note)
#     return 1


# async def notify_employee_head_epid_md(note: Note):
#     patient_id, patient_name, datetime_get, employee = await get_main_info(note=note)
#     md = get_md()
#     epids = get_epid()
#     epids_list = ""
#     epid_text = td.EMPLOYEE_AND_HEAD_AND_EPID_AND_MD["epid"].format(
#         name=employee.name,
#         department=employee.department.name,
#         md="qwe"
#     )
#     for epid in epids:
#         epids_list += f"{epid.name}, "
#         await try_send_message(chat_id=epid.telegram_id, text=epid_text)
#
#     print(employee.department)
#     head = employee.department.head
#     employee_text = td.EMPLOYEE_AND_HEAD_AND_EPID_AND_MD["employee"].format(
#         patient_id=patient_id,
#         patient_name=patient_name,
#         datetime_get=datetime_get,
#         head=head.name,
#         epid=epids_list,
#         md=md.name,
#     )
#     head_text = td.EMPLOYEE_AND_HEAD_AND_EPID["head"].format(
#         name=employee.name,
#         patient_name=patient_name,
#         patient_id=patient_id,
#         datetime_get=datetime_get,
#         epid=epids_list,
#         md=md.name
#     )
#     md_text = td.EMPLOYEE_AND_HEAD_AND_EPID_AND_MD["md"].format(
#         name=employee.name,
#         department=employee.department.name
#     )
#     await try_send_message(chat_id=employee.telegram_id, text=employee_text)
#     await try_send_message(chat_id=head.telegram_id, text=head_text)
#     await try_send_message(chat_id=md.telegram_id, text=md_text)
#     return 1


async def get_main_info(note: Note):
    return note.patient_id, note.patient_name, note.datetime_get, note.employee


async def try_send_message(chat_id: int, text: str, keyboard=None):
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard
        )
    except Exception as e:
        print(traceback.format_exc())


NOTIFY_BY_COUNT = {
    1: notify_employee_and_head,
    # 2: notify_employee_head_epid,
    # 3: notify_employee_head_epid_md,
}
