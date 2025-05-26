from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.user.paginator import Paginator
from app.config import settings


class Callback_kb_user(CallbackData, prefix = 'user'):
    level : int | None = None
    menu_name : str | None = None
    page : int | None = None
    command : str | None = None
    booking_id : int | None = None

def user_kb_main(user_id : int, size : tuple[int] = (1,)):
    kb = InlineKeyboardBuilder()
    button = [InlineKeyboardButton(text="🍽️ Забронировать столик", callback_data= Callback_kb_user(
                                                                    level = 1,
                                                                    menu_name = 'booking').pack()),
              InlineKeyboardButton(text="📅 Мои брони", callback_data=Callback_kb_user(
                  level=2,
                  menu_name='my_bookings').pack()),
              InlineKeyboardButton(text="ℹ️ О нас", callback_data=Callback_kb_user(
                  level=0,
                  menu_name='about').pack())
              ]
    for a in button:
        kb.add(a)
    if user_id in settings.ADMIN_IDS:
        kb.add(InlineKeyboardButton(text="🔐 Админ-панель", callback_data= Callback_kb_user(
                                                                   menu_name = "admin_panel").pack()))
    kb.adjust(*size)
    return kb.as_markup()

def pages(paginator: Paginator):
    btns = dict()
    if paginator.has_previous():
        btns["◀ Пред."] = "previous"

    if paginator.has_next():
        btns["След. ▶"] = "next"

    return btns

def paginator_kb(page : int,
                    paginator_page : dict[str,str],
                    booking_id : int,
                    level : int,
                    sizes : tuple[int] = (2,)):
    kb = InlineKeyboardBuilder()


    row_2 = []
    for text, menu_name in paginator_page.items():
        if menu_name == 'next':
            row_2.append(InlineKeyboardButton(text=text,
                                            callback_data=Callback_kb_user(
                                                page=page + 1,
                                                level=level
                                            ).pack()))
        if menu_name == 'previous':
            row_2.append(InlineKeyboardButton(text=text,
                                            callback_data=Callback_kb_user(
                                                page=page - 1,
                                                level=level
                                            ).pack()))

    kb.row(*row_2)

    row_3 = [InlineKeyboardButton(text='Удалить',
                                 callback_data= Callback_kb_user(level = level,
                                                               page = page,
                                                               command = 'delete',
                                                               booking_id = booking_id).pack())]
    kb.row(*row_3)

    row_4 = [InlineKeyboardButton(text='Назад',
                                 callback_data=Callback_kb_user(level= 0,
                                                             menu_name='main').pack()),
            ]

    kb.row(*row_4)
    return kb.adjust(*sizes).as_markup()

def return_kb_cart():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Назад', callback_data=Callback_kb_user(level= 0,
                                                                          menu_name='main').pack()))
    kb.adjust()
    return kb.as_markup()




