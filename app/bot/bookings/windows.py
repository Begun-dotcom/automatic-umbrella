from datetime import timezone

from aiogram_dialog import Window
import operator
from datetime import date

from aiogram_dialog.widgets.common import Scroll
from aiogram_dialog.widgets.kbd import Group, Button, Cancel, ScrollingGroup, Select, Back, Calendar, CalendarConfig
from aiogram_dialog.widgets.text import Const, Format
from asyncpg.pgproto.pgproto import timedelta

from app.bot.bookings.getters import get_all_tables, get_capacity, get_all_available_slots, get_confirmed_data, \
    getter_my_booking, get_info
from app.bot.bookings.state import BookingState, MyBookingState, AdminState
from app.bot.bookings.state_handler import process_add_count_capacity, on_table_select, cancel_logic_kb, \
    process_date_selected, process_slots_selected, select_ok_btn, click_my_booking, count_user


def get_capacity_window() -> Window:
    return Window(
        Const(text="Выберите кол-во гостей:"),
        Group(Select(
            text=Format("{item[0]}"),
            id="capacity_select",
            item_id_getter=lambda item: str(item[0]),
            items="capacity",
            on_click=process_add_count_capacity),
            id= 'group_capacity',
            width= 2),
        Group( Cancel(Const("Отмена"),
                                           on_click=cancel_logic_kb),
                                           width=2),
        getter=get_capacity,
        state=BookingState.count
    )
def get_table_window():
    return Window(
        Format("{text_table}"),
        ScrollingGroup(Select(
            text=Format("Стол № {item[id]} - {item[description]}"),
            id= "table_select",
            item_id_getter=lambda item : str(item["id"]),
            items="tables",
            on_click=on_table_select
        ),
            id="tables_scrolling",
            width=1,
            height=1,),
        Group(Back(Const("Назад")), Cancel(Const("Отмена"), on_click=cancel_logic_kb), width= 2),
        getter=get_all_tables,
        state=BookingState.table
    )

def get_date_window():
    return Window(
        Const(text="На какой день бронируем столик?"),
        Calendar(
            id = "cal",
            on_click=process_date_selected,
            config=CalendarConfig(
                firstweekday=0,
                timezone=timezone(timedelta(hours=3)),
                min_date=date.today())
        ),
        Back(Const("Назад")),
        Cancel(Const("Отмена"), on_click=cancel_logic_kb),
        state=BookingState.date
    )
def get_slots_window():
    return Window(
        Format("{text_table}"),
        ScrollingGroup(
            Select(
                Format("{item[start_time]} до {item[stop_time]}"),
                id = "slot_select",
                item_id_getter= lambda item : str(item["id"]),
                items="free_slot",
                on_click=process_slots_selected

            ),
            id= "slot_scroll",
            height=3,
            width=2

        ),
        Cancel(Const("Отмена"), on_click= cancel_logic_kb),
                     Back(Const("Назад")),
        getter=get_all_available_slots,
        state=BookingState.time
    )
def get_confirmed_windows():
    return Window(
        Format('{text}'),
        Group(Button(Const('Все верно?'),
                     id = 'select_ok',
                     on_click=select_ok_btn),
              Back(Const('Назад')),
              Cancel(Const('Отмена'), on_click= cancel_logic_kb),
                     ),
        getter=get_confirmed_data,
        state=BookingState.confirmation
    )
# -----------------------------------
def get_my_book():
    return Window(
        Format(text='{textt}'),
    ScrollingGroup(
        Select(
            Format("{item}"),
        id='select_my_book',
        item_id_getter=operator.itemgetter(13,14),
        items='text',
        on_click=click_my_booking,
            ),
        id= 'scroll_my_book',
        height=1,
        width=1
        ),
        Cancel(Const('Отмена'), on_click= cancel_logic_kb),
        getter=getter_my_booking,
        state= MyBookingState.booking
     )

# ---------------------------------------
def admin_dialog_menu_window():
    return Window(
        Const('Выберите дальнейшее действие:'),
        Group(
            Button(Const("📊 Статистика по пользователям"), id='1', on_click=count_user,),
            Button(Const("📈 Статистика по броням"), id='2', on_click=count_user),
        ), Cancel(Const('Отмена'), on_click=cancel_logic_kb),
        state=AdminState.menu
    )
def admin_count_user():
    return Window(
        Format("{admin}"),
        Back(Const("Назад")),
        Cancel(Const("Отмена"), on_click=cancel_logic_kb),
        getter=get_info,
        state=AdminState.user_count
    )



