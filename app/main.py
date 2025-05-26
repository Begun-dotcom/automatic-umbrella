from contextlib import asynccontextmanager

import uvicorn
from aiogram.types import Update
from fastapi import FastAPI, Request
from loguru import logger

from app.api.api_router import faststream_router, disable_booking
from app.bot.creat_bot import start_bot, stop_bot, bot, dp
from app.config import settings, broker, scheduler


@asynccontextmanager
async def lifespan (app:FastAPI):
    logger.info("Бот запускается...")
    await start_bot()
    await broker.start()
    scheduler.start()
    scheduler.add_job(
        func=disable_booking,
        id="clean_booking",
        trigger='interval',
        minutes = 1,
        replace_existing=True
    )
    await bot.set_webhook(url=settings.get_webhook,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    logger.success(f"Вебхук установлен: {settings.get_webhook}")
    yield
    logger.info("Бот остановлен...")
    await broker.close()
    scheduler.shutdown()
    await stop_bot()




app = FastAPI(lifespan=lifespan)
app.include_router(faststream_router)
@app.post('/webhook')
async def webhook(request : Request):
    try:
        update_data = await request.json()
        update = Update.model_validate(obj=update_data, context={bot : 'bot'})
        await dp.feed_update(bot=bot, update=update)
        logger.info(f'Обновления {update} успешно обработаны')
    except Exception as e:
        logger.error(f'Ошибка обновления обновлений {e}')

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1',port=8000)