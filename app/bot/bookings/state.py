from aiogram.fsm.state import StatesGroup, State


class BookingState(StatesGroup):
    count = State()
    table = State()
    date = State()
    time = State()
    confirmation = State()
    success = State()

class MyBookingState(StatesGroup):
    booking = State()

class AdminState(StatesGroup):
    menu = State()
    user_count = State()
