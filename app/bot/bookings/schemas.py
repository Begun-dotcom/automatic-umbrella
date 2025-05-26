from pydantic import BaseModel, ConfigDict
from datetime import date


class Table_capacity_schemas(BaseModel):
    capacity : int

    model_config = ConfigDict(from_attributes=True)

class Table_id_schemas(BaseModel):
    id : int

class Tables_schema_orm(BaseModel):
    id : int
    name: str|None
    description: str
    capacity: int

    model_config = ConfigDict(from_attributes=True)

class booking_table_all_schemas(BaseModel):
    table_id: int
    date: date

class Time_slot_schemas(BaseModel):
    id : int
    start_time: str
    stop_time: str

    model_config = ConfigDict(from_attributes=True)


class Time_slot_by_id(BaseModel):
    id: int

class Booking_all_check_schemas(BaseModel):
    timeslot_id: int
    table_id : int
    date : date

class Booking_add_user(BaseModel):
    user_telegram_id : int
    timeslot_id: int
    table_id : int
    date : date
    status : str

class User_count_schemas(BaseModel):
    id : int




