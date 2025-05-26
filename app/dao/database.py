from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from app.config import settings

URL = settings.get_url_database
async_engine = create_async_engine(url=URL)

async_session_maker = async_sessionmaker(bind=async_engine, class_= AsyncSession)


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created : Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated : Mapped[datetime] = mapped_column(TIMESTAMP, server_default= func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(self):
        return self.__name__.lower() + 's'
