from aiogram import Dispatcher
from aiogram.dispatcher import filters
from . import commands
from ..filters import NotEmployee


def setup(dp: Dispatcher):
    dp.register_message_handler(commands.start_message, filters.CommandStart())
    dp.register_message_handler(commands.show_stat_by_role, filters.Text("Статистика"))
    dp.register_message_handler(commands.total_stat_by_depart, filters.Text("Статистика по отделам"), NotEmployee())
    dp.register_message_handler(commands.show_short_stat, filters.Text("Краткая сводка по больнице"),
                                NotEmployee())
    dp.register_message_handler(commands.show_dep_lost_deadline_count, filters.Text("Просрочки по отделам"),
                                NotEmployee())
    # dp.register_message_handler(commands.total_stat_by_depart, filters.Text("Статистика по пользователям"),
    #                             NotEmployee())
