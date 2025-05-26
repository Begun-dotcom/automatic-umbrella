from typing import List
from datetime import date
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base


class main_menu(Base):
    name : Mapped[str]
    description : Mapped[str]


class User(Base):
    telegram_id : Mapped[int] = mapped_column(BigInteger, unique= True)
    user_name: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    bookings : Mapped[List['Booking']] = relationship(
        'Booking',
        back_populates='user',
        cascade= 'all, delete-orphan'
    )
    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username='{self.user_name}')>"


class Timeslot(Base):
    start_time : Mapped[str|None]
    stop_time : Mapped[str|None]
    bookings : Mapped[List['Booking']] = relationship(
        'Booking',
        back_populates='timeslot',
        cascade='all, delete-orphan'
    )
    def __repr__(self):
        return f"<Time(id={self.id}, start_time={self.start_time}, stop_time='{self.stop_time}')>"

class Table(Base):
    name : Mapped[str|None]
    description : Mapped[str|None]
    capacity : Mapped[int|None]
    bookings : Mapped[List['Booking']] = relationship(
        'Booking',
        back_populates='table',
        cascade= 'all, delete-orphan'
    )
    def __repr__(self):
        return f"<Table(id = {self.id}, name={self.name}, description={self.description}, capacity='{self.capacity}')>"

class Booking(Base):
    user_telegram_id : Mapped[int] = mapped_column(ForeignKey('users.telegram_id'))
    timeslot_id : Mapped[int] = mapped_column(ForeignKey('timeslots.id'))
    table_id : Mapped[int] = mapped_column(ForeignKey('tables.id'))
    date: Mapped[date]
    status: Mapped[str]
    user : Mapped['User'] = relationship(
        "User",
        back_populates='bookings'
    )
    timeslot : Mapped['Timeslot'] = relationship(
        'Timeslot',
        back_populates='bookings'
    )
    table : Mapped['Table'] = relationship(
        'Table',
        back_populates='bookings'
    )
    def __repr__(self):
        return f"<Booking(user_telegram_id={self.user_telegram_id}, timeslot_id={self.timeslot_id}, status='{self.status}')>"

