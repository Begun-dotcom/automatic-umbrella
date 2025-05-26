from aiogram import Router, F, types
from aiogram_dialog import DialogManager, StartMode

from app.bot.admin.admin_filter import AdminFilters
from app.bot.bookings.state import AdminState
from app.bot.user.user_kb import Callback_kb_user

admin_router = Router()

admin_router.message.filter(AdminFilters())

@admin_router.callback_query(Callback_kb_user.filter(F.menu_name == 'admin_panel'))
async def adm_panel(call : types.CallbackQuery, dialog_manager : DialogManager):
     await call.answer('Вы вошли в панель администратора')
     await dialog_manager.start(state=AdminState.menu, mode=StartMode.RESET_STACK)