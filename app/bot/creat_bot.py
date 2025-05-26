import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram_dialog import setup_dialogs
from loguru import logger

from app.bot.admin.admin_router import admin_router
from app.bot.bookings.dialogs import booking_dialog, my_booking_dialog, admin_dialog
from app.dao.middleware import DatabaseMiddlewareWithCommit, DatabaseMiddlewareWithoutCommit

from app.bot.user.user_router import user_router
from app.config import settings
from app.utils import add_db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

async def bot_command():
    command = [BotCommand(command='start', description='Стартуем')]
    await bot.set_my_commands(command, BotCommandScopeDefault())



async def start_bot():
    if settings.INIT_DB:
        await add_db()
    await bot_command()
    setup_dialogs(dp)
    dp.update.middleware.register(DatabaseMiddlewareWithCommit())
    dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_router(admin_dialog)
    dp.include_router(booking_dialog)
    dp.include_router(my_booking_dialog)
    try:
        for admin_id in settings.ADMIN_IDS:
            await bot.send_message(chat_id=admin_id, text='Бот успешно запущен 🍻\n'
                                                          'Для лучшей работы нажмите Старт')
    except:
        pass
    logger.info('Бот запущен')



async def stop_bot():
    try:
        for admin_id in settings.ADMIN_IDS:
            await bot.send_message(chat_id=admin_id, text='Бот остановлен ❌')
    except:
        pass
    logger.error('Бот остановлен')


