from typing import Any

from aiogram import types
from datetime import date
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from app.bot.bookings.schemas import Table_capacity_schemas, Table_id_schemas, Tables_schema_orm, \
    booking_table_all_schemas, Time_slot_schemas, Time_slot_by_id, Booking_all_check_schemas, Booking_add_user
from app.bot.user.user_kb import user_kb_main
from app.config import broker
from app.dao.dao import TableDao, BookingDao, TimeslotDao, UserDao


async def cancel_logic_kb(call : types.CallbackQuery, button : Button, dialog_manager : DialogManager):
    await call.answer("Сценарий бронирования отменен!")
    await call.message.answer("Вы отменили сценарий бронирования.",
                                  reply_markup=user_kb_main(call.from_user.id))


async def process_add_count_capacity(call : types.CallbackQuery, widget : Any, dialog_manager : DialogManager, item_id : str):
    print(item_id)
    session = dialog_manager.middleware_data['session_with_commit']
    capacity = int(item_id)
    dialog_manager.dialog_data['capacity'] = capacity
    dialog_manager.dialog_data['table'] = [Tables_schema_orm.model_validate(a).model_dump()for a in await TableDao(session).get_table(Table_capacity_schemas(capacity = capacity))]
    await call.answer(f"Выбрано {capacity} гостей")
    await dialog_manager.next()

async def on_table_select(call : types.CallbackQuery, widget, dialog_manager : DialogManager, item_id : str):
    session = dialog_manager.middleware_data['session_with_commit']
    table_id = int(item_id)
    selected_table =  await TableDao(session).get_table_by_id(filters=Table_id_schemas(id = table_id))
    dialog_manager.dialog_data['select_table'] = Tables_schema_orm.model_validate(selected_table).model_dump()
    await call.answer(f"Выбран стол №{table_id} на {selected_table.capacity} мест")
    await dialog_manager.next()

async def process_date_selected(call : types.CallbackQuery, widget, dialog_manager : DialogManager, select_date : date):
    session = dialog_manager.middleware_data['session_with_commit']
    dialog_manager.dialog_data['select_data'] = select_date
    selected_table = dialog_manager.dialog_data['select_table']
    time_select_table = await BookingDao(session).get_free_time_slot(filters=booking_table_all_schemas(table_id=selected_table['id'],
                                                                                       date=select_date))
    if time_select_table:
        await call.answer(f"Выбрана дата: {select_date}")
        dialog_manager.dialog_data["slots"] = [Time_slot_schemas.model_validate(time).model_dump() for time in time_select_table]
        print(dialog_manager.dialog_data['slots'])
        await dialog_manager.next()
    else:
        await call.answer(f"Нет мест на {select_date} для стола №{selected_table.id}!")
        await dialog_manager.back()

async def process_slots_selected(call : types.CallbackQuery, widget, dialog_manager : DialogManager, item_id : str):
    time_slot_id = int(item_id)
    session = dialog_manager.middleware_data['session_with_commit']
    time = await TimeslotDao(session).get_time_by_id(Time_slot_by_id(id = time_slot_id))
    dialog_manager.dialog_data['select_time'] = Time_slot_schemas.model_validate(time).model_dump()

    await call.answer(f'Выбрано время с{time.start_time} по {time.stop_time}')
    await dialog_manager.next()

async def select_ok_btn(call : types.CallbackQuery, widget, dialog_manager : DialogManager):
    await call.message.delete()
    session = dialog_manager.middleware_data['session_with_commit']
    select_table = dialog_manager.dialog_data['select_table']
    select_time = dialog_manager.dialog_data['select_time']
    select_date = dialog_manager.dialog_data['select_data']
    print(f'{select_table}\n, {select_time}, \n {select_date}')
    check = await BookingDao(session).check_booking(Booking_all_check_schemas(
    timeslot_id=select_time.get('id', 0),
    table_id =select_table.get('id', 0),
    date =select_date))
    if check is False:
        await call.answer('Приступаю к сохранению')
        await BookingDao(session).add_booking(Booking_add_user(user_telegram_id=call.from_user.id,
                                                                             timeslot_id=select_time.get('id', None),
                                                                             table_id=select_table.get('id', None),
                                                                             date=select_date,
                                                                             status='booked'))

        admin_text = (f'Столик № {select_table['id']} пользователем {call.from_user.first_name}\n'
                      f'забронирован на {select_date} с {select_time.get('start_time', 0)} по {select_time.get('stop_time', 0)}')
        await broker.publish(message='hello', queue="admin_msg")

        await broker.publish(admin_text,'admin')
        await broker.publish(call.from_user.id,'user')
        await call.message.answer('Столик успешно забронирован!', reply_markup=user_kb_main(call.from_user.id))
        await dialog_manager.done()



    else:
        await call.answer(
            f'На дату {select_date}\nВремя с{select_time.get('start_time', 0)} по {select_time.get('stop_time', 0)}\n'
            f'к сожалению уже занято\nВыберите пожалуйста другое время')
        await dialog_manager.back()



# ---------------------------------------
async def click_my_booking(call : types.CallbackQuery, widget : Any, dialog_manager : DialogManager, item_id : str):
    print(item_id, 'aa')

# ----------------------------------------
async def count_user(call : types.CallbackQuery, button : Button, dialog_manager : DialogManager):
    button_id = button.widget_id
    session = dialog_manager.middleware_data['session_with_commit']
    print(session)
    text = ''
    if button_id == '1':
        print('a')
        count_users = await UserDao(session).get_count_user()
        text = f'Общее количество пользователей: {count_users}'
        print(text)
    elif button_id == '2':
        book_table = await BookingDao(session).get_all_book()
        text = (f'Всего бронирований: {book_table.get('count', 0)}\n\n'
                f'Активные: {book_table.get('booked', 0)}\n\n'
                f'Отмененные: {book_table.get('canceled', 0)}')
        print(text)

    dialog_manager.dialog_data['admin'] = text
    await dialog_manager.next()
