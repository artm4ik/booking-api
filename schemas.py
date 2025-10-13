from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from models import UserRole, RoomType

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class HotelBase(BaseModel):
    name: str
    city: str
    stars: int

class HotelCreate(HotelBase):
    pass

class HotelResponse(HotelBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    room_type: RoomType
    price: float
    rooms_count: int
    max_people: int

class RoomCreate(RoomBase):
    hotel_id: int

class RoomResponse(RoomBase):
    id: int
    hotel_id: int
    is_available: bool

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    room_id: int
    start_date: datetime
    end_date: datetime

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    user_id: int
    total_days: int
    created_at: datetime

    class Config:
        from_attributes = True

class FlightBase(BaseModel):
    departure_city: str
    arrival_city: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    total_seats: int
    available_seats: int

class FlightCreate(FlightBase):
    pass

class FlightResponse(FlightBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FlightTicketBase(BaseModel):
    flight_id: int
    passengers_count: int

class FlightTicketCreate(FlightTicketBase):
    pass

class FlightTicketResponse(FlightTicketBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FlightSearch(BaseModel):
    departure_city: str
    arrival_city: str
    departure_date: datetime
    passengers_count: int

class HotelSearch(BaseModel):
    city: Optional[str] = None
    stars: Optional[int] = None
    check_in: datetime
    check_out: datetime
    people_count: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    email: Optional[str] = None