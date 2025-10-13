from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from auth import get_current_active_user
from models import User, Booking, Room, UserRole
from schemas import BookingResponse, BookingCreate
from crud import create_booking

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", response_model=BookingResponse)
def create_booking_endpoint(
        booking: BookingCreate,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    if not room or not room.is_available:
        raise HTTPException(status_code=400, detail="Room not available")

    existing_booking = db.query(Booking).filter(
        Booking.room_id == booking.room_id,
        Booking.start_date < booking.end_date,
        Booking.end_date > booking.start_date
    ).first()

    if existing_booking:
        raise HTTPException(status_code=400, detail="Room already booked for these dates")

    total_days = (booking.end_date - booking.start_date).days

    db_booking = Booking(
        user_id=current_user.id,
        room_id=booking.room_id,
        start_date=booking.start_date,
        end_date=booking.end_date,
        total_days=total_days
    )

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@router.get("/my", response_model=List[BookingResponse])
def get_my_bookings(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    return db.query(Booking).filter(Booking.user_id == current_user.id).all()


@router.delete("/{booking_id}")
def cancel_booking(
        booking_id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if current_user.role != UserRole.ADMIN and booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db.delete(booking)
    db.commit()
    return {"message": "Booking cancelled"}