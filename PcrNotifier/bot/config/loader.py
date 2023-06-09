from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from PcrNotifier import settings

bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
storage = JSONStorage(f'{Path.cwd()}/{"fsm_data.json"}')
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()
