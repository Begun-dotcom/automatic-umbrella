import os.path
from typing import List
from urllib.parse import quote
from loguru import logger
from pydantic_settings import SettingsConfigDict, BaseSettings
from faststream.rabbit.fastapi import RabbitBroker
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
class Setting(BaseSettings):
    #db
    DB_HOST : str
    DB_PORT : int
    DB_NAME : str
    DB_USER : str
    DB_PASSWORD : int

    #bot
    BOT : str
    ADMIN_IDS : List[int]
    INIT_DB : bool

    #localtunnel
    BASE_URL : str

    #rabbit
    RABBITMQ_USERNAME : str
    RABBITMQ_PASSWORD : str
    RABBITMQ_HOST : str
    RABBITMQ_PORT : int
    VHOST : str

    #logger
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"
    STORE_URL: str = 'sqlite:///data/jobs.sqlite'

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','.env'))

    @property
    def get_webhook(self):
        return f'{self.BASE_URL}/webhook'

    @property
    def get_url_database(self):
        return (f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@'
                f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')

    @property
    def get_url_rabbit(self):
        return (
            f"amqp://{self.RABBITMQ_USERNAME}:{quote(self.RABBITMQ_PASSWORD)}@"
            f"{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.VHOST}")

settings = Setting()
scheduler = AsyncIOScheduler(jobstores={'default' : SQLAlchemyJobStore(url=settings.STORE_URL)})
broker = RabbitBroker(url=settings.get_url_rabbit)
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..', 'log.txt')
logger.add(log_file, level='INFO', format=settings.FORMAT_LOG, rotation=settings.LOG_ROTATION)