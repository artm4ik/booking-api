from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from auth import get_current_active_user
from models import User, Hotel, Room, UserRole
from schemas import HotelResponse, HotelCreate, RoomResponse, RoomCreate, HotelSearch
from crud import create_hotel, create_room

router = APIRouter(prefix="/hotels", tags=["hotels"])

@router.get("/", response_model=List[HotelResponse])
def get_hotels(
    city: Optional[str] = None,
    stars: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Hotel)
    if city:
        query = query.filter(Hotel.city == city)
    if stars:
        query = query.filter(Hotel.stars == stars)
    return query.order_by(Hotel.stars.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=HotelResponse)
def create_hotel_endpoint(
        hotel: HotelCreate,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_hotel = Hotel(
        name=hotel.name,
        city=hotel.city,
        stars=hotel.stars
    )
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

@router.get("/{hotel_id}/rooms", response_model=List[RoomResponse])
def get_hotel_rooms(
    hotel_id: int,
    room_type: Optional[str] = None,
    max_price: Optional[float] = None,
    min_people: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Room).filter(Room.hotel_id == hotel_id)
    if room_type:
        query = query.filter(Room.room_type == room_type)
    if max_price:
        query = query.filter(Room.price <= max_price)
    if min_people:
        query = query.filter(Room.max_people >= min_people)
    return query.order_by(Room.price).offset(skip).limit(limit).all()

@router.post("/{hotel_id}/rooms", response_model=RoomResponse)
def create_room_endpoint(
    hotel_id: int,
    room: RoomCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    room.hotel_id = hotel_id
    return create_room(db=db, room=room)