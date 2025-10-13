from database import SessionLocal, engine, Base
from models import User, Hotel, Room, Flight, UserRole, RoomType
from auth import get_password_hash
from datetime import datetime, timedelta

def create_fresh_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        admin = User(
            email="admin@example.com",
            name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN
        )
        db.add(admin)

        user = User(
            email="user@example.com",
            name="Regular User",
            hashed_password=get_password_hash("user123"),
            role=UserRole.USER
        )
        db.add(user)

        hotels_data = [
            {"name": "Grand Hotel", "city": "Moscow", "stars": 5},
            {"name": "Comfort Inn", "city": "Moscow", "stars": 3},
            {"name": "Seaside Resort", "city": "Sochi", "stars": 4},
        ]

        hotels = []
        for hotel_data in hotels_data:
            hotel = Hotel(**hotel_data)
            db.add(hotel)
            hotels.append(hotel)

        db.commit()

        rooms_data = [
            {"hotel_id": hotels[0].id, "room_type": RoomType.PREMIUM, "price": 15000, "rooms_count": 1, "max_people": 2},
            {"hotel_id": hotels[0].id, "room_type": RoomType.STANDARD, "price": 8000, "rooms_count": 1, "max_people": 2},
            {"hotel_id": hotels[1].id, "room_type": RoomType.STANDARD, "price": 5000, "rooms_count": 1, "max_people": 2},
            {"hotel_id": hotels[2].id, "room_type": RoomType.LARGE, "price": 12000, "rooms_count": 2, "max_people": 4},
        ]

        for room_data in rooms_data:
            room = Room(**room_data)
            db.add(room)

        flights_data = [
            {"departure_city": "Moscow", "arrival_city": "Sochi", "departure_time": datetime.now() + timedelta(days=1), "arrival_time": datetime.now() + timedelta(days=1, hours=3), "price": 8000, "total_seats": 180, "available_seats": 150},
            {"departure_city": "Moscow", "arrival_city": "Sochi", "departure_time": datetime.now() + timedelta(days=2), "arrival_time": datetime.now() + timedelta(days=2, hours=4), "price": 6000, "total_seats": 180, "available_seats": 180},
            {"departure_city": "Moscow", "arrival_city": "Saint Petersburg", "departure_time": datetime.now() + timedelta(days=1), "arrival_time": datetime.now() + timedelta(days=1, hours=1), "price": 4000, "total_seats": 120, "available_seats": 100},
        ]

        for flight_data in flights_data:
            flight = Flight(**flight_data)
            db.add(flight)

        db.commit()
        print("Fresh test data created successfully!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_fresh_data()