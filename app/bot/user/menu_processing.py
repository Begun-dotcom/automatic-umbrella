
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.user.paginator import Paginator
from app.bot.user.user_kb import user_kb_main, pages, paginator_kb, return_kb_cart
from app.dao.dao import Main_menuDao, BookingDao
from aiogram import types
from app.schemas.schemas import Menu_name_schemas, My_Booking_det_schemas, Booking_updated_schemas


async def get_main_menu(level : int, menu_name : str, session : AsyncSession, user_id : int):
    text = await Main_menuDao(session).get_content_menu(Menu_name_schemas(name = menu_name))
    kb = user_kb_main(user_id=user_id)
    return text, kb



# --------------------------------level 2
async def get_my_bookings(session : AsyncSession, user_id : int, page : int,
                          booking_id : int, level : int, command : str, call : types.CallbackQuery):
    if page is None:
        page = 1
    if command == 'delete':
        print(booking_id)
        await BookingDao(session).update_booking_state(Booking_updated_schemas(id = booking_id))
        await call.answer('Бронирование отменено')
        if page > 1:
            page -= 1
    my_bookings = await BookingDao(session).get_my_bookings(My_Booking_det_schemas(user_telegram_id=user_id,
                                                                                       status='booked'))
    if not my_bookings:
        text = 'У Вас не активных броней'
        kb = return_kb_cart()
        return text, kb
    paginator = Paginator(array=my_bookings, page = page)
    get_page = paginator.get_page()[0]
    text = (f"📅 Дата бронирования: {get_page.date.strftime('%d/%m/%y')}\n\n"
            f"🍽 Информация о столике :\n\n"
            f"-📝 Описание: {get_page.table.description}\n"
            f"-👥 Вместимость: {get_page.table.capacity}\n"
            f"-#️⃣ Номер столика: {get_page.table_id}\n\n"
            f"Время бронирования:\n\n"
            f"⏰ с {get_page.timeslot.start_time} - {get_page.timeslot.stop_time}\n\n"
            f"Страница{paginator.page} из {paginator.pages}")
    paginator_page = pages(paginator)
    kb =  paginator_kb(page=page, paginator_page=paginator_page,
                       booking_id=get_page.id,
                       level=level)
    return text, kb







async def get_content(level : int, menu_name : str, session : AsyncSession,
                      user_id : int, page : int| None = None, booking_id : int | None = None,
                      command : str | None = None, call : types.CallbackQuery | None = None):
    if level == 0:
        return await get_main_menu(level=level, menu_name=menu_name, session=session, user_id= user_id)
    elif level == 2:
        return await get_my_bookings(session=session, user_id=user_id, page=page,
                                     booking_id=booking_id,level=level, command = command, call = call)


