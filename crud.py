from sqlalchemy.orm import Session
from models import User, Hotel, Room, Booking, Flight, FlightTicket
from auth import get_password_hash
from schemas import UserCreate, HotelCreate, RoomCreate, BookingCreate, FlightCreate

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_hotel(db: Session, hotel: HotelCreate):
    db_hotel = Hotel(**hotel.dict())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def get_hotels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Hotel).offset(skip).limit(limit).all()

def create_room(db: Session, room: RoomCreate):
    db_room = Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Room).offset(skip).limit(limit).all()

def create_booking(db: Session, booking: BookingCreate, user_id: int):
    db_booking = Booking(**booking.dict(), user_id=user_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def create_flight(db: Session, flight: FlightCreate):
    db_flight = Flight(**flight.dict())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight

def get_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Flight).offset(skip).limit(limit).all()