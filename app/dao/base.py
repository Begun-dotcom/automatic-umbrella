from typing import Type,List

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import TypeVar, Generic

from app.dao.database import Base

T = TypeVar('T', bound=Base)

class BaseDao(Generic[T]):
    model : Type[T] = None

    def __init__(self, session : AsyncSession):
        self._session = session
        if self._session is None:
            raise ValueError("Модель должна быть указана в дочернем классе")

    async def add_all(self, data: List[dict]):
        try:
            self._session.add_all([self.model(**a) for a in data])
            logger.info(f'{self.model.__name__} прошло успешно')
            await self._session.commit()
        except SQLAlchemyError as e:
            await self._session.rollback()
            logger.error(f'Error {e}')

