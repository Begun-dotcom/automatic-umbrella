from datetime import datetime, timedelta

from faststream.rabbit.fastapi import RabbitRouter
from loguru import logger

from app.bot.creat_bot import bot
from app.config import settings, scheduler
from app.dao.dao import BookingDao
from app.dao.database import async_session_maker

faststream_router = RabbitRouter(url=settings.get_url_rabbit)

@faststream_router.subscriber("admin")
async def adm_queue(msg : str):
    for admin in settings.ADMIN_IDS:
        await bot.send_message(chat_id=admin, text=msg)


async def send_user_msg(text : str, user_id : int):
    await bot.send_message(chat_id=user_id, text=text)


@faststream_router.subscriber("user")
async def user_queue(user_id:int):
    now = datetime.now()
    notifications = [
        {'time': now + timedelta(seconds=30),
         "text": "Спасибо за выбор нашего ресторана! Мы надеемся, вам понравится. "
                 "Оставьте отзыв, чтобы мы стали лучше! 😊"

         },
        {'time': now + timedelta(seconds=50),
         "text": "Не хотите забронировать столик снова? Попробуйте наше новое меню! 🍽️"

         },
        {'time': now + timedelta(minutes=2),
         "text": "Специально для вас! Скидка 10% на следующее посещение по промокоду WELCOMEBACK. 🎉"

         },
        {'time': now + timedelta(hours=24),
         "text": "Мы ценим ваше мнение! Расскажите о своем опыте и получите приятный бонус! 🎁"

         },
    ]
    for i, notification in enumerate(notifications):
        job_id = f'notifications user {user_id}_{i}'
        scheduler.add_job(
            func=send_user_msg,
            trigger='date',
            run_date=notification['time'],
            args= [notification['text'], user_id],
            id= job_id,
            replace_existing=True

        )
        logger.info(
            f"Запланировано уведомление для пользователя {user_id} на {notification['time']}")

async def disable_booking():
    async with async_session_maker() as session:
        await BookingDao(session).complete_past_bookings()





