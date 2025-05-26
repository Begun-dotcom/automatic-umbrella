from loguru import logger
from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.sql.functions import count

from app.dao.base import BaseDao
from app.dao.model import User, Timeslot, Table, Booking, main_menu


class UserDao(BaseDao[User]):
    model = User

    async def get_user(self, filters : BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        query = select(self.model).filter_by(**filter_dict)
        logger.info(f'Выполняется запрос в {self.model.__name__} с параметрами{filter_dict}')
        try:
            request = await self._session.execute(query)
            result = request.scalar_one_or_none()
            logger.info(f'Запрос в {self.model.__name__} выполнен успешно')
            return result
        except SQLAlchemyError as e:
            logger.error(f'Error {e}')
            raise

    async def add_user(self, filters : BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        self._session.add(self.model(**filter_dict))
        logger.info(f'Выполняется добавление в {self.model.__name__} с параметрами{filter_dict}')
        try:
            await self._session.flush()
            logger.info(f'Добавление в {self.model.__name__} выполнен успешно')
        except SQLAlchemyError as e:
            logger.error(f'Error {e}')
            raise

    async def get_count_user(self):
        query = select(count(self.model.id))
        logger.info(f'Выполняется запрос в {self.model.__name__}')
        try:
            request = await self._session.execute(query)
            result = request.scalar()
            logger.info(f'Запрос в {self.model.__name__} выполнен успешно')
            return result
        except SQLAlchemyError as e:
            logger.error(f'Error {e}')
            raise


class TimeslotDao(BaseDao[Timeslot]):
    model = Timeslot

    async def get_time_by_id(self, filters : BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        query = select(self.model).filter_by(**filter_dict)
        logger.info(f'Выполняется запрос в {self.model.__name__} с параметрами{filter_dict}')
        try:
            result = await self._session.execute(query)
            logger.info(f'Запрос в {self.model.__name__} выполнен успешно')
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f'Error {e}')
            raise

class TableDao(BaseDao[Table]):
    model = Table

    async def get_table(self, filters : BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        query = select(self.model).filter_by(**filter_dict)
        logger.info(f'Выполняется запрос в {self.model.__name__} с параметрами{filter_dict}')
        try:
            request = await self._session.execute(query)
            result = request.scalars().all()
            logger.info(f'Запрос в {self.model.__name__} выполнен успешно')
            return result
        except SQLAlchemyError as e:
            logger.error(f'Error {e}')
            raise

    async def get_table_by_id(self, filters : BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        query = select(self.model).filter_by(**filter_dict)
        logger.info(f'Выполняется запрос в {self.model.__name__} по параметрам{filter_dict}')
        try:
            result = await self._session.execute(query)
            logger.info(f'Запрос в {self.model.__name__} выполнен успешно')
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f'Error {e}')
            raise

    async def get_capacity(self):
        query = select(self.model.capacity).order_by(self.model.capacity)
        try:
            result = await self._session.execute(query)
            return result.scalars()
        except SQLAlchemyError as e:
            logger.error(e)
            raise e




class BookingDao(BaseDao[Booking]):
    model = Booking

    async def get_free_time_slot(self, filters : BaseModel):
        filters_dict = filters.model_dump(exclude_unset=True)
        query = select(self.model).filter_by(**filters_dict)

        try:
            table_all_on_date = await self._session.execute(query)
            result = table_all_on_date.scalars().all()
            booked = [booked.timeslot_id for booked in result if booked.status == 'booked']
            time_query = select(Timeslot).filter(
                ~Timeslot.id.in_(booked)
            )
            result_time = await self._session.execute(time_query)
            return result_time.scalars().all()
        except SQLAlchemyError as e:
            raise e

    async def check_booking(self, filters : BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        query = select(self.model).filter_by(**filter_dict)
        logger.info(f'Выполняется запрос в {self.model.__name__} по параметрам{filter_dict}')
        try:
            result = await self._session.execute(query)
            logger.info(f'Запрос в {self.model.__name__} выполнен успешно')
            if not result.scalars().all():
                return False
            for book in result.scalars().all():
                if book.status == "booked":
                    return True
                continue
            return False

        except SQLAlchemyError as e:
            logger.error(f'Error {e}')
            raise

    async def add_booking(self, filters : BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        self._session.add(self.model(**filter_dict))
        try:
            await self._session.flush()
            logger.info(f'Запись в {self.model.__name__} с параметрами {filter_dict} успешно добавлена')
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    async def get_my_bookings(self, filters : BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        query = select(self.model).filter_by(**filter_dict).options(selectinload(self.model.table),
                                                                    selectinload(self.model.timeslot))
        logger.info(f'Выполняется запрос в {self.model.__name__} с параметрами{filter_dict}')
        try:
            request = await self._session.execute(query)
            result = request.scalars().all()
            logger.info(f'Запрос в {self.model.__name__} выполнен успешно')
            return result
        except SQLAlchemyError as e:
            logger.error(f'Error {e}')
            raise

    async def update_booking_state(self, filters : BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        query = update(self.model).filter_by(**filter_dict).values(status  = "canceled")
        logger.info(f'Выполняется запрос в {self.model.__name__} с параметрами{filter_dict}')
        try:
            await self._session.execute(query)
            await self._session.flush()
            logger.info(f'Обновление в {self.model.__name__} на статус "canceled" выполнен успешно')
        except SQLAlchemyError as e:
            await self._session.rollback()
            logger.error(f'Error {e}')
            raise

    async def get_all_book(self):
        status_book = ['booked',"canceled"]
        count_book = {}
        for status in status_book:
            query = select(count(self.model.id)).filter(self.model.status == status)
            try:
                result = await self._session.execute(query)
                count_book[status] = result.scalar()
            except SQLAlchemyError as e:
                logger.error(f'Error {e}')
                raise
        query = select(count(self.model.id))
        result = await self._session.execute(query)
        count_book['count'] = result.scalar()
        return count_book

    async def complete_past_bookings(self):
        date = datetime.today()
        times = date.strftime('%H:%M')
        get_time = select(Timeslot.stop_time).filter(self.model.timeslot_id == Timeslot.id).scalar_subquery()
        print(get_time)
        get_booking_id = (select(self.model.id).filter(self.model.date == date.date(), get_time < times).
                          union_all(select(self.model.id).filter(self.model.date < date.date())))
        try:
            query = delete(self.model).filter(self.model.id.in_(get_booking_id))
            await self._session.execute(query)
            await self._session.commit()
            logger.info(f'Удалено {count(get_booking_id)} записей')
        except SQLAlchemyError as e:
            logger.error(f'Error {e}')
            raise
        # dates = datetime.today()
        # time = dates.strftime('%H:%M')
        # query = select(Timeslot.stop_time).filter(self.model.timeslot_id == Timeslot.id).scalar_subquery()
        # del_query = (delete(self.model.id).filter(self.model.date <= dates.date(), query < time))
        #              # .filter(self.model.date == dates.date())).
        # try:
        #     await self._session.execute(del_query)
        #     await self._session.commit()
        # except SQLAlchemyError as e:
        #     logger.error(f'Error {e}')
        #     raise


class Main_menuDao(BaseDao[main_menu]):
    model = main_menu

    async def get_content_menu(self, filters : BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        query = select(self.model).filter_by(**filter_dict)
        logger.info(f'Выполняется запрос в {self.model.__name__} с параметрами{filter_dict}')
        try:
            request = await self._session.execute(query)
            result = request.scalar_one_or_none()
            logger.info(f'Запрос в {self.model.__name__} выполнен успешно')
            return result.description
        except SQLAlchemyError as e:
            logger.error(f'Error {e}')
            raise



