

from aiogram_dialog import DialogManager

from app.dao.dao import TableDao, BookingDao

from app.schemas.schemas import My_Booking_det_schemas


async def get_capacity(dialog_manager : DialogManager, **kwargs):
    session = dialog_manager.middleware_data['session_with_commit']
    capacity = await TableDao(session).get_capacity()
    capt_table = [capacity for capacity in capacity]
    real_capa = capt_table[-1]
    a = [[str(b)] for b in range(1, real_capa + 1)]
    text = {'capacity' : a}
    return text


async def get_all_tables(dialog_manager : DialogManager, **kwargs):
    tables = dialog_manager.dialog_data['table']
    capacity = dialog_manager.dialog_data['capacity']
    text = {'tables' : tables,
            'text_table' : f'для {capacity} человек {len(tables)} найдено столов'}
    print(text)
    return text

async def get_all_available_slots(dialog_manager : DialogManager, **kwargs):
    select_table = dialog_manager.dialog_data["select_table"]
    select_data = dialog_manager.dialog_data['select_data']
    time_slot = dialog_manager.dialog_data["slots"]
    print(time_slot)
    text = {"text_table" : f'Для стола {select_table['description']} на дату {select_data} доступно следующее свободно время, \nсделайте выбор',
            "free_slot" : time_slot}
    return text

async def get_confirmed_data(dialog_manager : DialogManager, **kwargs):
    select_table = dialog_manager.dialog_data['select_table']
    select_data = dialog_manager.dialog_data['select_data']
    select_time = dialog_manager.dialog_data['select_time']
    text = (f"🗓 Подтверждение бронирования\n\n"
            f"📅 Дата бронирования: {select_data.strftime('%d/%m/%y')}\n\n"
            f"🍽 Информация о столике :\n\n"
            f"-📝 Описание: {select_table.get('description', 'None')}\n"
            f"-👥 Вместимость: {select_table.get('capacity', 'None')}\n"
            f"-#️⃣ Номер столика: {select_table.get('id', 'None')}\n\n"
            f"Время бронирования:\n\n"
            f"⏰ с {select_time['start_time']} - {select_time['stop_time']}\n\n"
            f"✅ Все верно?")
    return {'text' : text}

# ----------------------------------------
async def getter_my_booking(dialog_manager : DialogManager, **kwargs):
    session = dialog_manager.middleware_data["session_with_commit"]
    user_id = 5368126539
    my_bookings = await BookingDao(session).get_my_bookings(My_Booking_det_schemas(user_telegram_id=user_id,
                                                                                   status='booked'))
    texts = {}

    list_text = []
    if not my_bookings:
        text = 'У Вас не активных броней'
        list_text.append(text)
        return texts
    for my_bookings in my_bookings:
        text =  (f"Ваша бронь № {my_bookings.id}"
                 f"📅 Дата бронирования: {my_bookings.date.strftime('%d/%m/%y')}\n\n"
                f"🍽 Информация о столике :\n\n"
                f"-📝 Описание: {my_bookings.table.description}\n"
                f"-👥 Вместимость: {my_bookings.table.capacity}\n"
                f"-#️⃣ Номер столика: {my_bookings.table_id}\n\n"
                f"Время бронирования:\n\n"
                f"⏰ с {my_bookings.timeslot.start_time} - {my_bookings.timeslot.stop_time}\n\n")
            # {'id' : f'{my_bookings.id}',
            #     'data' : f"📅 Дата бронирования: {my_bookings.date.strftime('%d/%m/%y')}",
            #     "description":f"-📝 Описание: {my_bookings.table.description}",
            #     "capacity" :f"-👥 Вместимость: {my_bookings.table.capacity}",
            #     "count": f"-#️⃣ Номер столика: {my_bookings.table_id}",
            #     "time_info":f"⏰ с {my_bookings.timeslot.start_time} - {my_bookings.timeslot.stop_time}"}
        list_text.append(text)

    text_test = (f"Ваша бронь № {my_bookings.id}"
            f"📅 Дата бронирования: {my_bookings.date.strftime('%d/%m/%y')}\n\n"
            f"🍽 Информация о столике :\n\n"
            f"-📝 Описание: {my_bookings.table.description}\n"
            f"-👥 Вместимость: {my_bookings.table.capacity}\n"
            f"-#️⃣ Номер столика: {my_bookings.table_id}\n\n"
            f"Время бронирования:\n\n"
            f"⏰ с {my_bookings.timeslot.start_time} - {my_bookings.timeslot.stop_time}\n\n")


    texts['text'] = list_text
    texts['textt'] = text_test
    print(texts)

    return texts

async def get_info(dialog_manager : DialogManager, **kwargs):
    text = dialog_manager.dialog_data['admin']
    return {'admin' : text}