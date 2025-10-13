from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
from auth import get_current_active_user
from models import User, Flight, FlightTicket, UserRole
from schemas import FlightResponse, FlightCreate, FlightTicketResponse, FlightTicketCreate, FlightSearch
from crud import create_flight

router = APIRouter(prefix="/flights", tags=["flights"])


@router.get("/", response_model=List[FlightResponse])
def get_flights(
        departure_city: Optional[str] = None,
        arrival_city: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    query = db.query(Flight)
    if departure_city:
        query = query.filter(Flight.departure_city == departure_city)
    if arrival_city:
        query = query.filter(Flight.arrival_city == arrival_city)
    return query.order_by(Flight.price).offset(skip).limit(limit).all()


@router.post("/", response_model=FlightResponse)
def create_flight_endpoint(
        flight: FlightCreate,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return create_flight(db=db, flight=flight)


@router.post("/search")
def search_flights(
        search: FlightSearch,
        db: Session = Depends(get_db)
):
    direct_flights = db.query(Flight).filter(
        Flight.departure_city == search.departure_city,
        Flight.arrival_city == search.arrival_city,
        Flight.departure_time >= search.departure_date,
        Flight.available_seats >= search.passengers_count
    ).all()

    results = []

    for flight in direct_flights:
        flight_data = FlightResponse.from_orm(flight)
        flight_dict = flight_data.dict()
        flight_dict["is_direct"] = True
        flight_dict["is_fastest"] = False
        flight_dict["is_cheapest"] = False
        results.append(flight_dict)

    if results:
        fastest = min(results, key=lambda x: (x["arrival_time"] - x["departure_time"]).total_seconds())
        cheapest = min(results, key=lambda x: x["price"])

        for result in results:
            if result["id"] == fastest["id"]:
                result["is_fastest"] = True
            if result["id"] == cheapest["id"]:
                result["is_cheapest"] = True

    return results


@router.post("/{flight_id}/book", response_model=FlightTicketResponse)
def book_flight(
        flight_id: int,
        ticket: FlightTicketCreate,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    if flight.available_seats < ticket.passengers_count:
        raise HTTPException(status_code=400, detail="Not enough seats available")

    flight.available_seats -= ticket.passengers_count

    db_ticket = FlightTicket(
        user_id=current_user.id,
        flight_id=flight_id,
        passengers_count=ticket.passengers_count
    )

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@router.get("/my-tickets", response_model=List[FlightTicketResponse])
def get_my_tickets(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    return db.query(FlightTicket).filter(FlightTicket.user_id == current_user.id).all()