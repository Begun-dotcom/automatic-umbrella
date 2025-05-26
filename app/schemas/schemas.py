from pydantic import BaseModel


class User_id_schemas(BaseModel):
    telegram_id : int

class Menu_name_schemas(BaseModel):
    name : str

class My_Booking_det_schemas(BaseModel):
    user_telegram_id : int
    status : str

class Booking_updated_schemas(BaseModel):
    id : int