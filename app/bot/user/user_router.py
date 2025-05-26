from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode
from click import command
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.bookings.state import BookingState, MyBookingState
from app.bot.user.menu_processing import get_content
from app.bot.user.user_kb import Callback_kb_user
from app.dao.dao import UserDao
from app.schemas.schemas import User_id_schemas

user_router = Router()

@user_router.message(CommandStart())
async def cms(message : types.Message, session_with_commit : AsyncSession):
    try:
        user = await UserDao(session_with_commit).get_user(User_id_schemas(telegram_id = message.from_user.id))
        if user is None:
            await UserDao(session_with_commit).add_user(User_id_schemas(telegram_id = message.from_user.id))

        text, kb = await get_content(level=0, menu_name='main',session=session_with_commit, user_id=message.from_user.id)
        await message.answer(text=text, reply_markup=kb)
    except Exception as e:
        raise e

@user_router.callback_query(Callback_kb_user.filter())
async def get_all_content(call : types.CallbackQuery, callback_data : Callback_kb_user,
                          session_with_commit:AsyncSession, dialog_manager : DialogManager):
    try:
        menu_name = callback_data.menu_name
        level = callback_data.level
        page = callback_data.page
        booking_id = callback_data.booking_id
        commands = callback_data.command
        if menu_name == 'booking':
            await call.answer('Бронирование стола')
            await dialog_manager.start(state=BookingState.count, mode=StartMode.RESET_STACK)
            return
        if menu_name == "my_bookings":
            await call.answer('Ваши брони')
            await dialog_manager.start(state=MyBookingState.booking, mode=StartMode.RESET_STACK)
            return
        text, kb = await get_content(level=level, menu_name=menu_name,
                                     session=session_with_commit, user_id=call.from_user.id,
                                     page=page, booking_id = booking_id, command=commands, call=call)
        await call.message.edit_text(text=text, reply_markup=kb)
    except Exception as e:
        await call.answer('')
        raise e




