from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="user")
    flight_tickets = relationship("FlightTicket", back_populates="user")

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city = Column(String)
    stars = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    rooms = relationship("Room", back_populates="hotel")

class RoomType(str, enum.Enum):
    STANDARD = "standard"
    LARGE = "large"
    PREMIUM = "premium"

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    room_type = Column(SQLEnum(RoomType))
    price = Column(Float)
    rooms_count = Column(Integer)
    max_people = Column(Integer)
    is_available = Column(Boolean, default=True)

    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    total_days = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    departure_city = Column(String)
    arrival_city = Column(String)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    price = Column(Float)
    total_seats = Column(Integer)
    available_seats = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    tickets = relationship("FlightTicket", back_populates="flight")

class FlightTicket(Base):
    __tablename__ = "flight_tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    flight_id = Column(Integer, ForeignKey("flights.id"))
    passengers_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="flight_tickets")
    flight = relationship("Flight", back_populates="tickets")